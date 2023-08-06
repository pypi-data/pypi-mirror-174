import importlib
from types import ModuleType
from typing import Any, List

import pluggy

from . import __name__ as pkgname
from . import hookspecs, settings


class PluginManager(pluggy.PluginManager):  # type: ignore[misc]
    @classmethod
    def get(cls, settings: settings.Settings) -> "PluginManager":
        hook_modules = (
            "postgresql",
            "instances",
            "databases",
            "passfile",
            "backup",
            "patroni",
            "pgbackrest",
            "prometheus",
            "powa",
            "temboard",
            "systemd.service_manager",
            "systemd.scheduler",
        )
        self = cls(pkgname)
        self.add_hookspecs(hookspecs)
        for hname in hook_modules:
            hm = importlib.import_module(f"{pkgname}.{hname}")
            if not hasattr(hm, "register_if") or hm.register_if(settings):
                self.register(hm)
        return self

    def unregister_all(self) -> List[ModuleType]:
        unregistered = []
        for __, plugin in self.list_name_plugin():
            self.unregister(plugin)
            unregistered.append(plugin)
        return unregistered

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.get_plugins() == other.get_plugins()  # type: ignore[no-any-return]
