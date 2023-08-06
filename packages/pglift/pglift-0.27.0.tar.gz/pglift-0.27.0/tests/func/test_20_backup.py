import pytest

from pglift import instances, systemd
from pglift.ctx import Context
from pglift.models import system
from pglift.systemd import scheduler


def test_systemd_backup_job(ctx: Context, instance: system.Instance) -> None:
    if ctx.settings.scheduler != "systemd":
        pytest.skip(f"not applicable for scheduler method '{ctx.settings.scheduler}'")

    unit = scheduler.unit("backup", instance.qualname)
    assert systemd.is_enabled(ctx, unit)

    assert not systemd.is_active(ctx, unit)
    with instances.running(ctx, instance):
        assert systemd.is_active(ctx, unit)
    assert not systemd.is_active(ctx, unit)
