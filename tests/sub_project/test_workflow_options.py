"""Tests for optional agent workflow integrations."""

from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import pytest
import yaml


def _read_toml(path: Path) -> dict:
    with path.open('rb') as file:
        return tomllib.load(file)


def test_default_excludes_workflow_options(sub_project: Path) -> None:
    assert not (sub_project / 'openspec').exists()
    assert not (sub_project / 'backlog').exists()
    assert not (sub_project / '.alint.yml').exists()
    assert not (sub_project / 'AGENTS.md').exists()

    mise = _read_toml(sub_project / 'mise.toml')
    assert set(mise['tools']) == {'uv', 'python'}
    assert {'format', 'format-check', 'type-check', 'quality'} <= set(mise['tasks'])

    pyproject = _read_toml(sub_project / 'pyproject.toml')
    assert 'mypy>=1.0,<2.0' in pyproject['dependency-groups']['dev']
    assert 'ruff>=0.17.0' in pyproject['dependency-groups']['dev']
    assert (sub_project / 'README.md').read_bytes().endswith(b'\n')


@pytest.mark.parametrize('sub_project', [{'include_openspec': True}], indirect=True)
def test_openspec_enabled(sub_project: Path) -> None:
    assert (sub_project / 'openspec/specs').is_dir()
    assert (sub_project / 'openspec/changes/archive').is_dir()
    config = yaml.safe_load((sub_project / 'openspec/config.yaml').read_text())
    assert config['schema'] == 'spec-driven'

    mise = _read_toml(sub_project / 'mise.toml')
    assert mise['tools']['npm:@fission-ai/openspec'] == '1.15.0'
    assert 'openspec init --tools agents' in mise['tasks']['install']['run']
    assert mise['tasks']['openspec-update']['run'] == 'openspec update'
    assert 'OpenSpec' in (sub_project / 'AGENTS.md').read_text()


@pytest.mark.parametrize(
    ('sub_project', 'task_management'),
    [
        ({'task_management': 'backlog-md'}, 'backlog-md'),
        ({'task_management': 'backlog-md-py'}, 'backlog-md-py'),
    ],
    indirect=['sub_project'],
)
def test_backlog_enabled(sub_project: Path, task_management: str) -> None:
    config = yaml.safe_load((sub_project / 'backlog/config.yml').read_text())
    assert config['projectName'] == 'your-template-name-copier-template'
    assert config['autoCommit'] is False
    assert (sub_project / 'backlog/tasks').is_dir()

    mise = _read_toml(sub_project / 'mise.toml')
    pyproject = _read_toml(sub_project / 'pyproject.toml')
    dev = pyproject['dependency-groups']['dev']
    agents = (sub_project / 'AGENTS.md').read_text()
    if task_management == 'backlog-md':
        assert mise['tools']['npm:backlog.md'] == '1.55.3'
        assert mise['tasks']['backlog-list']['run'] == 'backlog task list --plain'
        assert not any('backlog-md-py' in dependency for dependency in dev)
    else:
        assert 'npm:backlog.md' not in mise['tools']
        assert any(dependency.startswith('backlog-md-py==2.1.0') for dependency in dev)
        assert (
            mise['tasks']['backlog-list']['run']
            == 'uv run backlog-py task list --plain'
        )
    assert 'Do not edit files under `backlog/` directly' in agents


@pytest.mark.parametrize('sub_project', [{'include_alint': True}], indirect=True)
def test_alint_enabled(sub_project: Path) -> None:
    config = yaml.safe_load((sub_project / '.alint.yml').read_text())
    assert 'alint://bundled/oss-baseline@v1' in config['extends']

    mise = _read_toml(sub_project / 'mise.toml')
    assert mise['tools']['github:asamarts/alint'] == '0.20.1'
    assert 'alint-check' in mise['tasks']['quality']['depends']

    prek = _read_toml(sub_project / 'prek.toml')
    local_repos = [repo for repo in prek['repos'] if repo['repo'] == 'local']
    assert any(
        hook['id'] == 'alint-check' for repo in local_repos for hook in repo['hooks']
    )


@pytest.mark.parametrize(
    'sub_project',
    [{'include_openspec': True, 'task_management': 'backlog-md-py'}],
    indirect=True,
)
def test_openspec_and_backlog_can_be_combined(sub_project: Path) -> None:
    agents = (sub_project / 'AGENTS.md').read_text()
    assert (sub_project / 'openspec').is_dir()
    assert (sub_project / 'backlog').is_dir()
    assert 'Keep repository status in Backlog' in agents
    assert 'change-specific implementation checklists in OpenSpec' in agents
