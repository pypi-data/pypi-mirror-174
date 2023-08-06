import configparser
import datetime
import json
import os
import re
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Union,
    overload,
)

from dateutil.tz import gettz
from pgtoolkit import conf as pgconf

from .. import exceptions, postgresql, util
from ..models import interface
from ..task import task
from ..types import BackupType

if TYPE_CHECKING:
    from ..ctx import BaseContext
    from ..models import system
    from ..settings import PgBackRestSettings, Settings


def available(settings: "Settings") -> Optional["PgBackRestSettings"]:
    return settings.pgbackrest


def get_settings(settings: "Settings") -> "PgBackRestSettings":
    """Return settings for pgbackrest

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.pgbackrest is not None
    return settings.pgbackrest


def enabled(stanza: str, settings: "PgBackRestSettings") -> bool:
    return stanza_config(stanza, settings).exists()


def base_config(settings: "PgBackRestSettings") -> Path:
    return settings.configpath / "pgbackrest.conf"


def config_directory(settings: "PgBackRestSettings") -> Path:
    return settings.configpath / "conf.d"


def stanza_config(stanza: str, settings: "PgBackRestSettings") -> Path:
    return config_directory(settings) / f"{stanza}.conf"


def make_cmd(stanza: str, settings: "PgBackRestSettings", *args: str) -> List[str]:
    return [
        str(settings.execpath),
        f"--config-path={settings.configpath}",
        f"--stanza={stanza}",
    ] + list(args)


pgpath_rgx = re.compile(r"pg\d+-path")


def stanza(instance: "system.BaseInstance", settings: "PgBackRestSettings") -> str:
    """Return stanza read from configuration file.

    :param instance: the instance.

    :raises ~exceptions.ConfigurationError: if no stanza is found for instance among config files.
    """
    d = config_directory(settings)
    cp = configparser.ConfigParser()
    cp.read(d.glob("*.conf"))
    for section in cp.sections():
        for key, value in cp.items(section):
            if pgpath_rgx.match(key) and value == str(instance.datadir):
                return section
    raise exceptions.ConfigurationError(d, f"no stanza found for {instance.qualname}")


@overload
def backup_info(
    ctx: "BaseContext",
    stanza: str,
    settings: "PgBackRestSettings",
    *,
    backup_set: Optional[str] = None,
    output_json: Literal[False],
) -> str:
    ...


@overload
def backup_info(
    ctx: "BaseContext",
    stanza: str,
    settings: "PgBackRestSettings",
    *,
    backup_set: Optional[str] = None,
) -> List[Dict[str, Any]]:
    ...


def backup_info(
    ctx: "BaseContext",
    stanza: str,
    settings: "PgBackRestSettings",
    *,
    backup_set: Optional[str] = None,
    output_json: bool = True,
) -> Union[List[Dict[str, Any]], str]:
    """Call pgbackrest info command to obtain information about backups.

    Ref.: https://pgbackrest.org/command.html#command-info
    """
    args = []
    if backup_set is not None:
        args.append(f"--set={backup_set}")
    if output_json:
        args.append("--output=json")
    args.append("info")
    r = ctx.run(make_cmd(stanza, settings, *args), check=True)
    if not output_json:
        return r.stdout
    return json.loads(r.stdout)  # type: ignore[no-any-return]


@task("setting up pgBackRest")
def setup(
    ctx: "BaseContext",
    stanza: str,
    settings: "PgBackRestSettings",
    instance_config: pgconf.Configuration,
    datadir: Path,
) -> None:
    """Setup pgBackRest"""
    base_config_path = base_config(settings)
    if not base_config_path.exists():
        raise exceptions.SystemError(
            f"Missing base config file {base_config_path} for pgbackrest. "
            "Did you forget to run 'pglift site-configure'?"
        )
    stanza_confpath = stanza_config(stanza, settings)

    # Always use string values so that this would match with actual config (on
    # disk) that's parsed later on.
    config = {
        stanza: {
            "pg1-path": str(datadir),
            "pg1-port": str(instance_config.get("port", 5432)),
            "pg1-user": ctx.settings.postgresql.backuprole.name,
        },
    }
    unix_socket_directories = instance_config.get("unix_socket_directories")
    if unix_socket_directories:
        config[stanza]["pg1-socket-path"] = str(instance_config.unix_socket_directories)
    cp = configparser.ConfigParser()
    actual_config = {}
    if stanza_confpath.exists():
        cp.read(stanza_confpath)
        actual_config = {name: dict(cp.items(name)) for name in config}
    if config != actual_config:
        cp.read_dict(config)

        with stanza_confpath.open("w") as configfile:
            cp.write(configfile)


@task("upgrading pgBackRest stanza {stanza}")
def upgrade(
    ctx: "BaseContext",
    instance: "system.PostgreSQLInstance",
    stanza: str,
    settings: "PgBackRestSettings",
    password: Optional[str],
) -> None:
    """Upgrade stanza"""
    postgresql.check_status(ctx, instance, postgresql.Status.not_running)
    ctx.run(make_cmd(stanza, settings, "stanza-upgrade", "--no-online"), check=True)
    env = os.environ.copy()
    if password is not None:
        env["PGPASSWORD"] = password
    with postgresql.running(ctx, instance):
        env = ctx.settings.postgresql.libpq_environ(
            ctx, instance, ctx.settings.postgresql.backuprole.name, base=env
        )
        ctx.run(make_cmd(stanza, settings, "check"), check=True, env=env)


def postgresql_configuration(
    stanza: str, settings: "PgBackRestSettings"
) -> pgconf.Configuration:
    pgconfig = util.template("postgresql", "pgbackrest.conf").format(
        execpath=settings.execpath, configpath=settings.configpath, stanza=stanza
    )
    config = pgconf.Configuration()
    list(config.parse(pgconfig.splitlines()))
    return config


@setup.revert("deconfiguring pgBackRest")
def revert_setup(
    ctx: "BaseContext",
    stanza: str,
    settings: "PgBackRestSettings",
    instance_config: pgconf.Configuration,
    datadir: Path,
) -> None:
    """Un-setup pgBackRest.

    Remove stanza's log files, and configuration file.
    """
    for logf in settings.logpath.glob(f"{stanza}-*.log"):
        logf.unlink(missing_ok=True)
    stanza_config(stanza, settings).unlink(missing_ok=True)


@task("creating pgBackRest stanza for {instance}")
def init(
    ctx: "BaseContext",
    instance: "system.PostgreSQLInstance",
    stanza: str,
    settings: "PgBackRestSettings",
    password: Optional[str],
) -> None:
    env = os.environ.copy()
    if password is not None:
        env["PGPASSWORD"] = password
    with postgresql.running(ctx, instance):
        env = ctx.settings.postgresql.libpq_environ(
            ctx, instance, ctx.settings.postgresql.backuprole.name, base=env
        )
        ctx.run(make_cmd(stanza, settings, "start"), check=True)
        ctx.run(make_cmd(stanza, settings, "stanza-create"), check=True, env=env)
        ctx.run(make_cmd(stanza, settings, "check"), check=True, env=env)


@init.revert("deleting pgBackRest stanza for {instance}")
def revert_init(
    ctx: "BaseContext",
    instance: "system.PostgreSQLInstance",
    stanza: str,
    settings: "PgBackRestSettings",
    *args: Any,
) -> None:
    ctx.run(make_cmd(stanza, settings, "stop"), check=True)
    ctx.run(make_cmd(stanza, settings, "stanza-delete", "--force"), check=True)


def backup_command(
    instance: "system.BaseInstance",
    settings: "PgBackRestSettings",
    *,
    type: BackupType = BackupType.default(),
    start_fast: bool = True,
) -> List[str]:
    """Return the full pgbackrest command to perform a backup for ``instance``.

    :param type: backup type (one of 'full', 'incr', 'diff').

    Ref.: https://pgbackrest.org/command.html#command-backup
    """
    args = [
        f"--type={type.name}",
        "--log-level-console=info",
        "backup",
    ]
    if start_fast:
        args.insert(-1, "--start-fast")
    stanza_ = stanza(instance, settings)
    return make_cmd(stanza_, settings, *args)


@task("backing up instance with pgBackRest")
def backup(
    ctx: "BaseContext",
    instance: "system.PostgreSQLInstance",
    settings: "PgBackRestSettings",
    *,
    type: BackupType = BackupType.default(),
) -> None:
    """Perform a backup of ``instance``.

    :param type: backup type (one of 'full', 'incr', 'diff').

    Ref.: https://pgbackrest.org/command.html#command-backup
    """
    if instance.standby:
        raise exceptions.InstanceStateError("backup should be done on primary instance")

    ctx.run(
        backup_command(instance, settings, type=type),
        check=True,
        env=ctx.settings.postgresql.libpq_environ(
            ctx, instance, ctx.settings.postgresql.backuprole.name
        ),
    )


def expire_command(
    instance: "system.BaseInstance", settings: "PgBackRestSettings"
) -> List[str]:
    """Return the full pgbackrest command to expire backups for ``instance``.

    Ref.: https://pgbackrest.org/command.html#command-expire
    """
    stanza_ = stanza(instance, settings)
    return make_cmd(stanza_, settings, "--log-level-console=info", "expire")


@task("expiring pgBackRest backups")
def expire(
    ctx: "BaseContext", instance: "system.BaseInstance", settings: "PgBackRestSettings"
) -> None:
    """Expire a backup of ``instance``.

    Ref.: https://pgbackrest.org/command.html#command-expire
    """
    ctx.run(expire_command(instance, settings), check=True)


def _parse_backup_databases(info: str) -> List[str]:
    """Parse output of pgbackrest info --set=<label> and return the list of
    databases.

    This is only required until "pgbackrest info" accepts options --set and
    --output=json together.

    >>> set_info = '''stanza: 13-main
    ... status: ok
    ... cipher: none
    ...
    ... db (current)
    ...     wal archive min/max (13-1): 000000010000000000000001/000000010000000000000004
    ...
    ...     full backup: 20210121-153336F
    ...         timestamp start/stop: 2021-01-21 15:33:36 / 2021-01-21 15:33:59
    ...         wal start/stop: 000000010000000000000004 / 000000010000000000000004
    ...         database size: 39.6MB, backup size: 39.6MB
    ...         repository size: 4.9MB, repository backup size: 4.9MB
    ...         database list: bar (16434), foo (16401), postgres (14174)
    ...         symlinks:
    ...             pg_wal => /var/lib/pgsql/13/main/pg_wal_mnt/pg_wal
    ... '''
    >>> _parse_backup_databases(set_info)
    ['bar', 'foo', 'postgres']
    """
    dbs_pattern = re.compile(r"^\s*database list:\s*(.*)$")
    db_pattern = re.compile(r"(\S+)\s*\(.*")
    for line in info.splitlines():
        m = dbs_pattern.match(line)
        if m:
            return [
                re.sub(db_pattern, r"\g<1>", db.strip()) for db in m.group(1).split(",")
            ]
    return []


def iter_backups(
    ctx: "BaseContext", instance: "system.BaseInstance", settings: "PgBackRestSettings"
) -> Iterator[interface.InstanceBackup]:
    """Yield information about backups on an instance."""
    stanza_ = stanza(instance, settings)
    backups = backup_info(ctx, stanza_, settings)[0]["backup"]

    def started_at(entry: Any) -> float:
        return entry["timestamp"]["start"]  # type: ignore[no-any-return]

    for backup in sorted(backups, key=started_at, reverse=True):
        info_set = backup_info(
            ctx,
            stanza_,
            settings,
            backup_set=backup["label"],
            output_json=False,
        )
        databases = _parse_backup_databases(info_set)
        dtstart = datetime.datetime.fromtimestamp(backup["timestamp"]["start"])
        dtstop = datetime.datetime.fromtimestamp(backup["timestamp"]["stop"])
        yield interface.InstanceBackup(
            label=backup["label"],
            size=backup["info"]["size"],
            repo_size=backup["info"]["repository"]["size"],
            date_start=dtstart.replace(tzinfo=gettz()),
            date_stop=dtstop.replace(tzinfo=gettz()),
            type=backup["type"],
            databases=databases,
        )


def restore_command(
    instance: "system.BaseInstance",
    settings: "PgBackRestSettings",
    *,
    date: Optional[datetime.datetime] = None,
    backup_set: Optional[str] = None,
) -> List[str]:
    """Return the pgbackrest restore for ``instance``.

    Ref.: https://pgbackrest.org/command.html#command-restore
    """
    args = [
        "--log-level-console=info",
        # The delta option allows pgBackRest to handle instance data/wal
        # directories itself, without the need to clean them up beforehand.
        "--delta",
        "--link-all",
    ]
    if date is not None and backup_set is not None:
        raise exceptions.UnsupportedError(
            "date and backup_set are not expected to be both specified"
        )
    elif date is not None:
        target = date.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        args += ["--target-action=promote", "--type=time", f"--target={target}"]
    elif backup_set is not None:
        args += ["--target-action=promote", "--type=immediate", f"--set={backup_set}"]
    args.append("restore")
    stanza_ = stanza(instance, settings)
    return make_cmd(stanza_, settings, *args)


@task("restoring instance with pgBackRest")
def restore(
    ctx: "BaseContext",
    instance: "system.PostgreSQLInstance",
    settings: "PgBackRestSettings",
    *,
    label: Optional[str] = None,
    date: Optional[datetime.datetime] = None,
) -> None:
    """Restore an instance, possibly only including specified databases.

    The instance must not be running.

    Ref.: https://pgbackrest.org/command.html#command-restore
    """
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)

    cmd = restore_command(instance, settings, date=date, backup_set=label)
    ctx.run(cmd, check=True)


def env_for(
    instance: "system.Instance", settings: "PgBackRestSettings"
) -> Dict[str, str]:
    return {
        "PGBACKREST_CONFIG_PATH": str(settings.configpath),
        "PGBACKREST_STANZA": stanza(instance, settings),
    }
