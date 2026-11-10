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
    local['prek']('validate-config', sub_project / 'prek.toml')
