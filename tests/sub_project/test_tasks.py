"""Tests for the copier template using plumbum."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest
from plumbum import local
from plumbum.cmd import docker, mise, uv


def _docker_daemon_available() -> bool:
    code, _, _ = docker['info'].run(retcode=None)
    return code == 0


def _isolated_mise_env(sub_project: Path) -> dict[str, str]:
    """Hermetic mise for test subprocesses.

    Trusts the fixture and ignores the user's global mise config, which
    may declare tools that cannot install in this environment.
    """
    global_root = Path(tempfile.mkdtemp(prefix='mise-global-test-'))
    (global_root / 'config.toml').touch()
    return {
        'MISE_TRUSTED_CONFIG_PATHS': str(sub_project),
        'MISE_GLOBAL_CONFIG_ROOT': str(global_root),
    }


def test_dev_setup(sub_project: Path) -> None:
    with local.cwd(sub_project), local.env(**_isolated_mise_env(sub_project)):
        mise['run', '--skip-tools', 'install']()


@pytest.mark.skipif(
    not shutil.which('docker') or not _docker_daemon_available(),
    reason='docker daemon unavailable',
)
def test_docker_mounts(sub_project: Path) -> None:
    with local.cwd(sub_project), local.env(**_isolated_mise_env(sub_project)):
        mise['run', '--skip-tools', 'example-docker']()


def test_sub_project_tests(sub_project: Path) -> None:
    with local.cwd(sub_project), local.env(**_isolated_mise_env(sub_project)):
        uv['sync']()
        mise['run', '--skip-tools', 'test']()
