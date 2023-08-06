import argparse
import logging
from typing import Optional, Sequence

from . import exceptions, settings
from .cmd import Program
from .ctx import Context
from .exceptions import InstanceNotFound
from .models import system

parser = argparse.ArgumentParser(description="Start postgres for specified instance")
parser.add_argument(
    "instance",
    help="instance identifier as <version>-<name>",
)


def main(
    argv: Optional[Sequence[str]] = None,
    *,
    ctx: Optional[Context] = None,
) -> int:
    args = parser.parse_args(argv)
    if ctx is None:
        ctx = Context(settings=settings.SiteSettings())

    try:
        instance = system.PostgreSQLInstance.from_qualname(ctx, args.instance)
    except ValueError as e:
        parser.error(str(e))
    except InstanceNotFound as e:
        parser.exit(2, str(e))

    cmd = [str(instance.bindir / "postgres"), "-D", str(instance.datadir)]
    pidfile = (
        ctx.settings.postgresql.pid_directory
        / f"postgresql-{instance.version}-{instance.name}.pid"
    )
    try:
        Program(cmd, pidfile, capture_output=False)
    except exceptions.CommandError:
        return 1
    else:
        return 0


if __name__ == "__main__":  # pragma: nocover
    import sys

    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
