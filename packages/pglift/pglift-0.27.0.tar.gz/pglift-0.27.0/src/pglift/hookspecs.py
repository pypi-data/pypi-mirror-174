from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Type

import pluggy
from pgtoolkit.conf import Configuration

from . import __name__ as pkgname
from ._compat import TypeAlias

if TYPE_CHECKING:
    import click

    from .ctx import BaseContext
    from .models import interface
    from .models.system import BaseInstance, Instance, PostgreSQLInstance
    from .postgresql import Standby
    from .settings import Settings, SystemdSettings
    from .types import ConfigChanges, Manifest, ServiceManifest

hookspec = pluggy.HookspecMarker(pkgname)

FirstResult: TypeAlias = Optional[Literal[True]]


@hookspec  # type: ignore[misc]
def site_configure_install(settings: "Settings") -> None:
    """Global configuration hook."""


@hookspec  # type: ignore[misc]
def site_configure_uninstall(settings: "Settings") -> None:
    """Global configuration hook."""


@hookspec  # type: ignore[misc]
def install_systemd_unit_template(
    settings: "Settings", systemd_settings: "SystemdSettings", header: str = ""
) -> None:
    """Install systemd unit templates."""


@hookspec  # type: ignore[misc]
def uninstall_systemd_unit_template(
    settings: "Settings", systemd_settings: "SystemdSettings"
) -> None:
    """Uninstall systemd unit templates."""


@hookspec  # type: ignore[misc]
def cli() -> "click.Command":
    """Return command-line entry point as click Command (or Group) for the plugin."""


@hookspec  # type: ignore[misc]
def instance_cli(group: "click.Group") -> None:
    """Extend 'group' with extra commands from the plugin."""


@hookspec  # type: ignore[misc]
def system_lookup(ctx: "BaseContext", instance: "PostgreSQLInstance") -> Optional[Any]:
    """Look up for the satellite service object on system that matches specified instance."""


@hookspec  # type: ignore[misc]
def get(ctx: "BaseContext", instance: "Instance") -> Optional["ServiceManifest"]:
    """Return the description the satellite service bound to specified instance."""


@hookspec  # type: ignore[misc]
def interface_model() -> Type["ServiceManifest"]:
    """The interface model for satellite component provided plugin."""


@hookspec  # type: ignore[misc]
def instance_settings(
    ctx: "BaseContext", manifest: "interface.Instance", instance: "BaseInstance"
) -> Configuration:
    """Called before the PostgreSQL instance settings is written."""


@hookspec(firstresult=True)  # type: ignore[misc]
def standby_model() -> Type["Manifest"]:
    """The model for standby provided by a plugin.

    Only one implementation should be invoked so call order and returned value
    matter.

    If an implementation raises ValueError, registration of the
    'standby' field in interface Instance model will be skipped.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def instance_init_replication(
    ctx: "BaseContext",
    instance: "Instance",
    manifest: "interface.Instance",
    standby: "Standby",
) -> Optional[bool]:
    """Called before PostgreSQL datadir is created for a standby."""


@hookspec  # type: ignore[misc]
def instance_configure(
    ctx: "BaseContext",
    manifest: "interface.Instance",
    config: Configuration,
    changes: "ConfigChanges",
    creating: bool,
    upgrading: bool,
) -> None:
    """Called when the PostgreSQL instance got (re-)configured."""


@hookspec  # type: ignore[misc]
def instance_drop(ctx: "BaseContext", instance: "Instance") -> None:
    """Called when the PostgreSQL instance got dropped."""


@hookspec  # type: ignore[misc]
def instance_start(ctx: "BaseContext", instance: "Instance") -> None:
    """Called when the PostgreSQL instance got started."""


@hookspec  # type: ignore[misc]
def instance_stop(ctx: "BaseContext", instance: "Instance") -> None:
    """Called when the PostgreSQL instance got stopped."""


@hookspec  # type: ignore[misc]
def instance_env(ctx: "BaseContext", instance: "Instance") -> Dict[str, str]:
    """Return environment variables for instance defined by the plugin."""


@hookspec  # type: ignore[misc]
def instance_upgrade(
    ctx: "BaseContext", old: "PostgreSQLInstance", new: "PostgreSQLInstance"
) -> None:
    """Called when 'old' PostgreSQL instance got upgraded as 'new'."""


@hookspec  # type: ignore[misc]
def role_change(
    ctx: "BaseContext", role: "interface.BaseRole", instance: "PostgreSQLInstance"
) -> bool:
    """Called when 'role' changed in 'instance' (be it a create, an update or a deletion).

    Return True if any change happened during hook invocation.
    """


@hookspec  # type: ignore[misc]
def rolename(settings: "Settings") -> str:
    """Return the name of role used by a plugin."""


@hookspec  # type: ignore[misc]
def role(settings: "Settings", manifest: "interface.Instance") -> "interface.Role":
    """Return the role used by a plugin, to be created at instance creation."""


@hookspec  # type: ignore[misc]
def database(
    settings: "Settings", manifest: "interface.Instance"
) -> "interface.Database":
    """Return the database used by a plugin, to be created at instance creation."""


@hookspec(firstresult=True)  # type: ignore[misc]
def initdb(
    ctx: "BaseContext", manifest: "interface.Instance", instance: "BaseInstance"
) -> FirstResult:
    """Initialize a PostgreSQL database cluster.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def postgresql_conf(instance: "PostgreSQLInstance") -> Path:
    """Return path to editable postgresql.conf.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def postgresql_editable_conf(ctx: "BaseContext", instance: "BaseInstance") -> str:
    """Return the content of editable postgresql.conf.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def configure_postgresql(
    ctx: "BaseContext",
    manifest: "interface.Instance",
    configuration: Configuration,
    instance: "BaseInstance",
) -> Optional["ConfigChanges"]:
    """Configure PostgreSQL and return 'changes' to postgresql.conf.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def configure_auth(
    settings: "Settings", instance: "BaseInstance", manifest: "interface.Instance"
) -> FirstResult:
    """Configure authentication for PostgreSQL (pg_hba.conf, pg_ident.conf).

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def start_postgresql(
    ctx: "BaseContext", instance: "PostgreSQLInstance", foreground: bool, wait: bool
) -> FirstResult:
    """Start PostgreSQL for specified 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def stop_postgresql(
    ctx: "BaseContext",
    instance: "PostgreSQLInstance",
    mode: str,
    wait: bool,
    deleting: bool,
) -> FirstResult:
    """Stop PostgreSQL for specified 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def restart_postgresql(
    ctx: "BaseContext", instance: "Instance", mode: str, wait: bool
) -> FirstResult:
    """Restart PostgreSQL for specified 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def reload_postgresql(ctx: "BaseContext", instance: "Instance") -> FirstResult:
    """Reload PostgreSQL configuration for 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def promote_postgresql(
    ctx: "BaseContext", instance: "PostgreSQLInstance"
) -> FirstResult:
    """Promote PostgreSQL for 'instance'.

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def postgresql_service_name() -> str:
    """Return the system service name (e.g.  postgresql).

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def enable_service(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Enable a service

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def disable_service(
    ctx: "BaseContext", service: str, name: str, now: Optional[bool]
) -> FirstResult:
    """Disable a service

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def start_service(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Start a service for a plugin

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def stop_service(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Stop a service for a plugin

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def restart_service(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Restart a service for a plugin

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def schedule_service(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Schedule a job through timer

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def unschedule_service(
    ctx: "BaseContext", service: str, name: str, now: Optional[bool]
) -> FirstResult:
    """Unchedule a job

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def start_timer(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Start a timer

    Only one implementation should be invoked so call order and returned value
    matter.
    """


@hookspec(firstresult=True)  # type: ignore[misc]
def stop_timer(ctx: "BaseContext", service: str, name: str) -> FirstResult:
    """Stop a timer

    Only one implementation should be invoked so call order and returned value
    matter.
    """
