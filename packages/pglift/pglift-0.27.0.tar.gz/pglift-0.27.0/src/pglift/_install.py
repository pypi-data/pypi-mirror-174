import logging
import sys
from typing import TYPE_CHECKING, Optional

from . import plugin_manager, systemd, util
from .task import task

if TYPE_CHECKING:
    from .pm import PluginManager
    from .settings import Settings, SystemdSettings

logger = logging.getLogger(__name__)
POSTGRESQL_SERVICE_NAME = "pglift-postgresql@.service"
BACKUP_SERVICE_NAME = "pglift-backup@.service"
BACKUP_TIMER_NAME = "pglift-backup@.timer"


@task("installing systemd template unit for PostgreSQL")
def postgresql_systemd_unit_template(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    *,
    env: Optional[str] = None,
    header: str = "",
) -> None:
    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    content = systemd.template(POSTGRESQL_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        python=sys.executable,
        environment=environment,
        pid_directory=settings.postgresql.pid_directory,
    )
    systemd.install(
        POSTGRESQL_SERVICE_NAME,
        util.with_header(content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@postgresql_systemd_unit_template.revert(
    "uninstalling systemd template unit for PostgreSQL"
)
def revert_postgresql_systemd_unit_template(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    *,
    env: Optional[str] = None,
    header: str = "",
) -> None:
    systemd.uninstall(
        POSTGRESQL_SERVICE_NAME, systemd_settings.unit_path, logger=logger
    )


@task("installing systemd template unit and timer for PostgreSQL backups")
def postgresql_backup_systemd_templates(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    *,
    env: Optional[str] = None,
    header: str = "",
) -> None:
    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    service_content = systemd.template(BACKUP_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        environment=environment,
        python=sys.executable,
    )
    systemd.install(
        BACKUP_SERVICE_NAME,
        util.with_header(service_content, header),
        systemd_settings.unit_path,
        logger=logger,
    )
    timer_content = systemd.template(BACKUP_TIMER_NAME).format(
        # TODO: use a setting for that value
        calendar="daily",
    )
    systemd.install(
        BACKUP_TIMER_NAME,
        util.with_header(timer_content, header),
        systemd_settings.unit_path,
        logger=logger,
    )


@postgresql_backup_systemd_templates.revert(
    "uninstalling systemd template unit and timer for PostgreSQL backups"
)
def revert_postgresql_backup_systemd_templates(
    settings: "Settings",
    systemd_settings: "SystemdSettings",
    *,
    env: Optional[str] = None,
    header: str = "",
) -> None:
    systemd.uninstall(BACKUP_SERVICE_NAME, systemd_settings.unit_path, logger=logger)
    systemd.uninstall(BACKUP_TIMER_NAME, systemd_settings.unit_path, logger=logger)


def do(settings: "Settings", env: Optional[str] = None, header: str = "") -> None:
    pm = plugin_manager(settings)
    do_site_configure(pm, settings)
    do_systemd(pm, settings, env=env, header=header)


def do_site_configure(pm: "PluginManager", settings: "Settings") -> None:
    pm.hook.site_configure_install(settings=settings)


def do_systemd(
    pm: "PluginManager",
    settings: "Settings",
    env: Optional[str] = None,
    header: str = "",
) -> None:
    if settings.service_manager != "systemd":
        logger.warning("not using systemd as 'service_manager', skipping installation")
        return
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    postgresql_systemd_unit_template(settings, systemd_settings, env=env, header=header)
    pm.hook.install_systemd_unit_template(
        settings=settings, systemd_settings=systemd_settings, header=header
    )
    postgresql_backup_systemd_templates(
        settings, systemd_settings, env=env, header=header
    )
    systemd.daemon_reload(systemd_settings)


def undo(settings: "Settings") -> None:
    pm = plugin_manager(settings)
    undo_site_configure(pm, settings)
    undo_systemd(pm, settings)


def undo_site_configure(pm: "PluginManager", settings: "Settings") -> None:
    pm.hook.site_configure_uninstall(settings=settings)


def undo_systemd(pm: "PluginManager", settings: "Settings") -> None:
    if settings.service_manager != "systemd":
        logger.warning(
            "not using systemd as 'service_manager', skipping uninstallation"
        )
        return
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    revert_postgresql_backup_systemd_templates(settings, systemd_settings)
    pm.hook.uninstall_systemd_unit_template(
        settings=settings, systemd_settings=systemd_settings
    )
    revert_postgresql_systemd_unit_template(settings, systemd_settings)
    systemd.daemon_reload(systemd_settings)
