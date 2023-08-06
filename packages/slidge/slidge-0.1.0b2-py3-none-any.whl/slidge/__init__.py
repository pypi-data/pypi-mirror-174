import slixmpp.plugins

from .core.contact import LegacyContact, LegacyRoster
from .core.gateway import BaseGateway
from .core.session import BaseSession
from .util import (
    FormField,
    SearchResult,
    xep_0030,
    xep_0055,
    xep_0077,
    xep_0084,
    xep_0100,
    xep_0115,
    xep_0292,
    xep_0333,
    xep_0356,
    xep_0356_old,
    xep_0363,
    xep_0461,
)
from .util.db import GatewayUser, user_store

slixmpp.plugins.__all__.extend(
    ["xep_0055", "xep_0292_provider", "xep_0356", "xep_0356_old", "xep_0461"]
)

__all__ = [
    "BaseGateway",
    "BaseSession",
    "GatewayUser",
    "LegacyContact",
    "LegacyRoster",
    "FormField",
    "SearchResult",
    "user_store",
]
