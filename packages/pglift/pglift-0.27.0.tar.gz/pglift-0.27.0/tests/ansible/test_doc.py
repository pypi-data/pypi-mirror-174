import json
import pathlib
import subprocess
from typing import Any, Dict, Optional

import pytest


@pytest.mark.parametrize(
    "module",
    ["instance", "dsn_info", "role", "database", "postgres_exporter"],
    ids=lambda v: f"module:{v}",
)
def test(
    tmp_path: pathlib.Path,
    module: str,
    ansible_env: Dict[str, str],
    pgbackrest_available: bool,
    prometheus_execpath: Optional[pathlib.Path],
    temboard_execpath: Optional[pathlib.Path],
) -> None:
    env = ansible_env.copy()
    settings: Dict[str, Any] = {}
    if pgbackrest_available:
        settings["pgbackrest"] = {}
    if prometheus_execpath:
        settings["prometheus"] = {"execpath": str(prometheus_execpath)}
    else:
        pytest.skip("prometheus not available")
    if temboard_execpath:
        settings["temboard"] = {"execpath": str(temboard_execpath)}
    else:
        pytest.skip("temboard not available")
    with (tmp_path / "config.json").open("w") as f:
        json.dump(settings, f)
    env["SETTINGS"] = f"@{tmp_path / 'config.json'}"

    subprocess.check_call(["ansible-doc", f"dalibo.pglift.{module}"], env=env)
