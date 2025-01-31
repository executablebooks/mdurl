from __future__ import annotations

from collections import namedtuple

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import NamedTuple

    class URL(NamedTuple):
        protocol: str | None
        slashes: bool
        auth: str | None
        port: str | None
        hostname: str | None
        hash: str | None  # noqa: A003
        search: str | None
        pathname: str | None

else:
    URL = namedtuple(
        "URL",
        [
            "protocol",
            "slashes",
            "auth",
            "port",
            "hostname",
            "hash",
            "search",
            "pathname",
        ],
    )
