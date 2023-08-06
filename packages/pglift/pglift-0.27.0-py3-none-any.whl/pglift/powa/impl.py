from typing import TYPE_CHECKING, Optional

from .. import types

if TYPE_CHECKING:
    from ..settings import PowaSettings, Settings

# Extensions to load in shared_preload_libraries and to install.
# Order is important here, for example`pg_stat_statements` needs to be loaded
# before `pg_stat_kcache` in shared_preload_libraries
POWA_EXTENSIONS = [
    types.Extension.btree_gist,
    types.Extension.pg_qualstats,
    types.Extension.pg_stat_statements,
    types.Extension.pg_stat_kcache,
    types.Extension.powa,
]


def available(settings: "Settings") -> Optional["PowaSettings"]:
    return settings.powa
