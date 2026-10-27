"""Tests for optional agent workflow integrations."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import pytest
import yaml


def _read_toml(path: Path) -> dict:
    with path.open('rb') as file:
        return tomllib.load(file)


def _alint_extends(sub_project: Path) -> list[str]:
    config = yaml.safe_load((sub_project / '.alint.yml').read_text())
    return config['extends']


def test_default_excludes_workflow_options(sub_project: Path) -> None:
    assert not (sub_project / 'openspec').exists()
    assert not (sub_project / 'backlog').exists()
    assert not (sub_project / '.alint.yml').exists()
    assert not (sub_project / 'AGENTS.md').exists()

    mise = _read_toml(sub_project / 'mise.toml')
    assert set(mise['tools']) == {'uv', 'python'}
    assert {'format', 'format-check', 'type-check', 'quality'} <= set(mise['tasks'])
    assert mise['tasks']['format-check']['wait_for'] == ['lint']
    assert mise['tasks']['type-check']['wait_for'] == ['lint']
    assert (
        'jdx/mise-action'
        not in (sub_project / '.github/workflows/pre-commit.yml').read_text()
    )

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
    yamllint = yaml.safe_load((sub_project / '.yamllint.yaml').read_text())
    assert 'backlog/config.yml' in yamllint['ignore']

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
    assert _alint_extends(sub_project) == [
        'alint://bundled/oss-baseline@v1',
        'alint://bundled/python@v1',
        'alint://bundled/ci/github-actions@v1',
    ]

    mise = _read_toml(sub_project / 'mise.toml')
    assert mise['tools']['github:asamarts/alint'] == '0.20.1'
    assert 'alint-check' in mise['tasks']['quality']['depends']

    prek = _read_toml(sub_project / 'prek.toml')
    local_repos = [repo for repo in prek['repos'] if repo['repo'] == 'local']
    assert any(
        hook['id'] == 'alint-check' for repo in local_repos for hook in repo['hooks']
    )
    workflow = yaml.safe_load(
        (sub_project / '.github/workflows/pre-commit.yml').read_text()
    )
    steps = workflow['jobs']['pre-commit']['steps']
    mise_steps = [
        step for step in steps if step.get('uses', '').startswith('jdx/mise-action@')
    ]
    assert len(mise_steps) == 1
    assert re.fullmatch(r'jdx/mise-action@[0-9a-f]{40}', mise_steps[0]['uses'])
    assert mise_steps[0]['with'].get('install', True) is True
    assert mise_steps[0]['with']['install_args'] == 'github:asamarts/alint'
    assert steps.index(mise_steps[0]) < next(
        index
        for index, step in enumerate(steps)
        if step.get('uses', '').startswith('j178/prek-action@')
    )


@pytest.mark.parametrize(
    ('sub_project', 'expected'),
    [
        (
            {'include_alint': True, 'alint_profile': 'minimal'},
            [
                'alint://bundled/oss-baseline@v1',
                'alint://bundled/ci/github-actions@v1',
            ],
        ),
        (
            {'include_alint': True, 'alint_profile': 'python'},
            [
                'alint://bundled/oss-baseline@v1',
                'alint://bundled/python@v1',
                'alint://bundled/ci/github-actions@v1',
            ],
        ),
        (
            {'include_alint': True, 'alint_profile': 'python-agentic'},
            [
                'alint://bundled/oss-baseline@v1',
                'alint://bundled/python@v1',
                'alint://bundled/agent-hygiene@v1',
                'alint://bundled/agent-context@v1',
                'alint://bundled/ci/github-actions@v1',
            ],
        ),
    ],
    indirect=['sub_project'],
)
def test_alint_profiles(sub_project: Path, expected: list[str]) -> None:
    assert _alint_extends(sub_project) == expected


@pytest.mark.parametrize(
    'sub_project',
    [
        {
            'include_alint': True,
            'alint_profile': 'custom',
            'alint_extra_bundles': ['docs/adr', 'versioning'],
        }
    ],
    indirect=True,
)
def test_alint_custom_extras(sub_project: Path) -> None:
    assert _alint_extends(sub_project) == [
        'alint://bundled/oss-baseline@v1',
        'alint://bundled/docs/adr@v1',
        'alint://bundled/versioning@v1',
        'alint://bundled/ci/github-actions@v1',
    ]


@pytest.mark.parametrize(
    'sub_project',
    [
        {
            'include_alint': True,
            'vcs_platform': 'gitlab',
            'alint_profile': 'custom',
            'alint_extra_bundles': ['versioning'],
        }
    ],
    indirect=True,
)
def test_alint_ci_bundle_is_github_only(sub_project: Path) -> None:
    assert _alint_extends(sub_project) == [
        'alint://bundled/oss-baseline@v1',
        'alint://bundled/versioning@v1',
    ]


def test_alint_rejects_unknown_alias(
    sub_project_factory: Callable[[dict[str, Any] | None], Path],
) -> None:
    with pytest.raises(ValueError, match='Unknown alint bundle aliases: bogus'):
        sub_project_factory(
            {
                'include_alint': True,
                'alint_profile': 'custom',
                'alint_extra_bundles': ['bogus'],
            }
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
