import logging
from typing import TYPE_CHECKING

from . import exceptions, hookimpl, settings, types
from .models import system
from .pgbackrest import impl as pgbackrest

if TYPE_CHECKING:
    from .ctx import BaseContext
    from .models import interface


service_name = "backup"


@hookimpl
def instance_configure(ctx: "BaseContext", manifest: "interface.Instance") -> None:
    """Enable scheduled backup job for configured instance."""
    instance = system.Instance.system_lookup(ctx, (manifest.name, manifest.version))
    ctx.hook.schedule_service(ctx=ctx, service=service_name, name=instance.qualname)


@hookimpl
def instance_drop(ctx: "BaseContext", instance: system.Instance) -> None:
    """Disable scheduled backup job when instance is being dropped."""
    ctx.hook.unschedule_service(
        ctx=ctx, service=service_name, name=instance.qualname, now=True
    )


@hookimpl
def instance_start(ctx: "BaseContext", instance: system.Instance) -> None:
    """Start schedule backup job at instance startup."""
    ctx.hook.start_timer(ctx=ctx, service=service_name, name=instance.qualname)


@hookimpl
def instance_stop(ctx: "BaseContext", instance: system.Instance) -> None:
    """Stop schedule backup job when instance is stopping."""
    ctx.hook.stop_timer(ctx=ctx, service=service_name, name=instance.qualname)


# This entry point is used by systemd 'postgresql-backup@' service.
def main() -> None:
    import argparse

    from .ctx import Context

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "instance", metavar="<version>-<name>", help="instance identifier"
    )

    def do_backup(
        ctx: "BaseContext", instance: system.Instance, args: argparse.Namespace
    ) -> None:
        settings = pgbackrest.get_settings(ctx.settings)
        return pgbackrest.backup(
            ctx, instance, settings, type=types.BackupType(args.type)
        )

    parser.set_defaults(func=do_backup)
    parser.add_argument(
        "--type",
        choices=[t.name for t in types.BackupType],
        default=types.BackupType.default().name,
    )

    args = parser.parse_args()
    ctx = Context(settings=settings.SiteSettings())
    try:
        instance = system.PostgreSQLInstance.from_qualname(ctx, args.instance)
    except ValueError as e:
        parser.error(str(e))
    except exceptions.InstanceNotFound as e:
        parser.exit(2, str(e))
    args.func(ctx, instance, args)


if __name__ == "__main__":  # pragma: nocover
    logging.basicConfig(level=logging.INFO)
    main()
