import asyncio
from typing import TYPE_CHECKING, Any, Union

import discord as di

from slidge import *

if TYPE_CHECKING:
    from . import Contact, Gateway, Roster
    from .client import Discord


class Session(BaseSession["Contact", "Roster", "Gateway"]):
    discord: "Discord"
    ready_future: asyncio.Future[bool]
    delete_futures: dict[int, asyncio.Future[bool]]
    edit_futures: dict[int, asyncio.Future[bool]]
    send_futures: dict[int, asyncio.Future[bool]]
    send_lock: asyncio.Lock

    def post_init(self):
        from .client import Discord

        self.discord = Discord(self)
        self.ready_future = self.xmpp.loop.create_future()
        self.delete_futures = {}
        self.edit_futures = {}
        self.send_futures = {}
        self.send_lock = asyncio.Lock()

    @staticmethod
    def xmpp_msg_id_to_legacy_msg_id(i: str) -> Union[int, str]:
        try:
            return int(i)
        except ValueError:
            return i

    async def login(self):
        self.xmpp.loop.create_task(
            self.discord.start(self.user.registration_form["token"])
        )
        await self.ready_future
        for u in self.discord.users:
            if not isinstance(u, di.User):
                self.log.debug(f"Skipping %s", u)
                continue
            if not u.is_friend():
                self.log.debug(f"%s is not a friend", u)
                continue
            c = self.contacts.by_legacy_id(u.id)
            await c.update_info()
            await c.add_to_roster()
            # TODO: contribute to discord.py-self so that the presence information
            #       of relationships is parsed. logs show:
            #       'PRESENCE_UPDATE referencing an unknown guild ID: %s. Discarding.'
            #       https://github.com/dolfies/discord.py-self/blob/master/discord/state.py#L1044
            c.online()
        return f"Logged on as {self.discord.user}"

    async def send_text(self, t: str, c: "Contact", *, reply_to_msg_id=None):
        async with self.send_lock:
            mid = (
                await c.discord_user.send(
                    t,
                    reference=None
                    if reply_to_msg_id is None
                    else di.MessageReference(
                        message_id=reply_to_msg_id,
                        channel_id=c.direct_channel_id,
                    ),
                )
            ).id
        f = self.send_futures[mid] = self.xmpp.loop.create_future()
        await f
        return mid

    async def logout(self):
        await self.discord.close()

    async def send_file(self, u: str, c: "Contact", *, reply_to_msg_id=None):
        # discord clients inline previews of external URLs, so no need to actually send on discord servers
        await c.discord_user.send(u)

    async def active(self, c: "Contact"):
        pass

    async def inactive(self, c: "Contact"):
        pass

    async def composing(self, c: "Contact"):
        await c.discord_user.trigger_typing()

    async def paused(self, c: "Contact"):
        pass

    async def displayed(self, legacy_msg_id: str, c: "Contact"):
        if not isinstance(legacy_msg_id, int):
            self.log.debug("This is not a valid discord msg id: %s", legacy_msg_id)
            return
        u = c.discord_user
        channel: di.DMChannel = u.dm_channel
        if channel is None:
            return
        m = await channel.fetch_message(legacy_msg_id)
        self.log.debug("Message %s should be marked as read", m)
        # try:
        #     await m.ack()  # triggers 404, maybe does not work for DM?
        # except Exception as e:
        #     self.log.exception("Message %s should have been marked as read but this raised %s", m, e)

    async def correct(self, text: str, legacy_msg_id: Any, c: "Contact"):
        u = c.discord_user
        channel: di.DMChannel = u.dm_channel
        if channel is None:
            return
        m = await channel.fetch_message(legacy_msg_id)
        self.edit_futures[legacy_msg_id] = self.xmpp.loop.create_future()
        await m.edit(content=text)
        await self.edit_futures[legacy_msg_id]

    async def react(self, legacy_msg_id: int, emojis: list[str], c: "Contact"):
        u = c.discord_user
        channel: di.DMChannel = u.dm_channel
        if channel is None:
            return
        m = await channel.fetch_message(legacy_msg_id)

        legacy_reactions = set(self.get_my_legacy_reactions(m))
        xmpp_reactions = set(emojis)

        self.log.debug("%s vs %s", legacy_reactions, xmpp_reactions)
        for e in xmpp_reactions - legacy_reactions:
            await m.add_reaction(e)
        for e in legacy_reactions - xmpp_reactions:
            await m.remove_reaction(e, self.discord.user)

    async def retract(self, legacy_msg_id: Any, c: "Contact"):
        u = c.discord_user
        channel: di.DMChannel = u.dm_channel
        if channel is None:
            return
        m = await channel.fetch_message(legacy_msg_id)
        self.delete_futures[legacy_msg_id] = self.xmpp.loop.create_future()
        await m.delete()
        await self.delete_futures[legacy_msg_id]

    def update_reactions(self, message: di.Message):
        self.contacts.by_discord_user(message.channel.recipient).carbon_react(
            message.id, self.get_my_legacy_reactions(message)
        )

    @staticmethod
    def get_my_legacy_reactions(message: di.Message) -> list[str]:
        reactions = []
        for r in message.reactions:
            if r.me and not r.custom_emoji:
                reactions.append(r.emoji)

        return reactions

    async def search(self, form_values: dict[str, str]) -> SearchResult:
        pass
