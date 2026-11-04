"""Tests for template_style feature."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import pytest
import yaml
from plumbum import local


@pytest.mark.parametrize(
    ('sub_project', 'expected_var_start', 'expected_var_end'),
    [
        ({'template_style': 'jinja'}, '{{', '}}'),
        ({'template_style': 'square_brackets'}, '[[', ']]'),
    ],
    indirect=['sub_project'],
)
def test_template_style(
    sub_project: Path,
    expected_var_start: str,
    expected_var_end: str,
) -> None:
    """Test that template_style configures the correct delimiters."""
    copier_yml = sub_project / 'copier.yml'

    with copier_yml.open() as f:
        config = yaml.safe_load(f)

    envops = config.get('_envops', {})
    actual_var_start = envops.get('variable_start_string', '{{')
    actual_var_end = envops.get('variable_end_string', '}}')

    assert actual_var_start == expected_var_start
    assert actual_var_end == expected_var_end
    assert expected_var_start in config['_answers_file']
    assert expected_var_end in config['_answers_file']


def test_generated_prek_config_parses_and_leaves_lock_formatting_to_uv(
    sub_project_factory: Callable[[dict[str, Any] | None], Path],
) -> None:
    sub_project = sub_project_factory({'include_alint': True})
    config = tomllib.loads((sub_project / 'prek.toml').read_text())
    assert config['exclude'] == '^uv\\.lock$'
    assert [hook for repo in config['repos'] for hook in repo['hooks']] == [
        {'id': 'end-of-file-fixer'},
        {'id': 'trailing-whitespace'},
        {'id': 'check-added-large-files'},
        {'id': 'check-yaml'},
        {'id': 'check-toml'},
        {'id': 'check-json'},
        {'id': 'check-case-conflict'},
        {'id': 'check-executables-have-shebangs'},
        {'id': 'check-merge-conflict', 'args': ['--assume-in-merge']},
        {'id': 'gitleaks'},
        {'id': 'ruff-check', 'args': ['--fix']},
        {'id': 'ruff-format'},
        {'id': 'uv-lock'},
        {'id': 'yamllint', 'args': ['--strict']},
        {'id': 'shellcheck'},
        {'id': 'check-github-workflows', 'args': ['--verbose']},
        {'id': 'check-gitlab-ci', 'args': ['--verbose']},
        {
            'id': 'check-renovate',
            'args': ['--verbose'],
            'additional_dependencies': ['pyjson5'],
        },
        {'id': 'conventional-pre-commit', 'stages': ['commit-msg']},
        {
            'id': 'alint-check',
            'name': 'alint check',
            'entry': 'alint check',
            'language': 'system',
            'pass_filenames': False,
            'always_run': True,
        },
    ]
    local['prek']('validate-config', sub_project / 'prek.toml')
