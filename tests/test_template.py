"""Tests for the copier template."""

from __future__ import annotations

import json
import stat
from pathlib import Path
from typing import Any

import pytest
from copier import run_copy, run_update

from tests.helpers import git_save, is_git_repo_dirty


def test_copy_default(
    template_dir: Path,
    tmp_path: Path,
    mock_answers_required_without_defaults: dict[str, Any],
) -> None:
    worker = run_copy(
        str(template_dir),
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
        data=mock_answers_required_without_defaults,
        unsafe=True,  # set to False if unsafe features not needed for template
    )
    assert (tmp_path / worker.answers_relpath).exists()
    assert (tmp_path / 'prek.toml').exists()
    assert (tmp_path / '.yamllint.yaml').exists()
    assert (tmp_path / '.github' / 'workflows' / 'pre-commit.yml').exists()


@pytest.mark.skipif(is_git_repo_dirty(), reason='Fail on dirty repo')
def test_update_default(
    template_dir: Path,
    tmp_path: Path,
    mock_answers_required_without_defaults: dict[str, Any],
) -> None:
    worker = run_copy(
        str(template_dir),
        tmp_path,
        defaults=True,
        data=mock_answers_required_without_defaults,
        unsafe=True,
    )
    git_save(tmp_path)
    run_update(
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
        overwrite=True,  # The default when run via CLI
        answers_file=worker.answers_relpath,
        unsafe=True,  # set to False if unsafe features not needed for template
    )
    assert (tmp_path / worker.answers_relpath).exists()


@pytest.mark.parametrize(
    ('strategy', 'expect_config', 'expect_workflow', 'token_ref'),
    [
        ('github-app', True, False, None),
        ('actions-github-token', True, True, 'secrets.GITHUB_TOKEN'),
        ('actions-pat', True, True, 'secrets.RENOVATE_TOKEN'),
        ('none', False, False, None),
    ],
)
def test_tool_update_strategy(
    template_dir: Path,
    tmp_path: Path,
    mock_answers_required_without_defaults: dict[str, Any],
    strategy: str,
    expect_config: bool,
    expect_workflow: bool,
    token_ref: str | None,
) -> None:
    worker = run_copy(
        str(template_dir),
        tmp_path,
        vcs_ref='HEAD',
        defaults=True,
        data={
            **mock_answers_required_without_defaults,
            'tool_update_strategy': strategy,
        },
        unsafe=True,
    )
    renovate_json = tmp_path / 'renovate.json'
    assert renovate_json.exists() is expect_config
    if expect_config:
        config = json.loads(renovate_json.read_text())

    workflow = tmp_path / '.github' / 'workflows' / 'renovate.yml'
    assert workflow.exists() is expect_workflow
    if expect_workflow:
        content = workflow.read_text()
        assert token_ref is not None
        assert token_ref in content
        assert (
            'renovatebot/github-action@2804199d260ad00c1fae0e9e842888369391c776'
            in content
        )

    if expect_config:
        disable_rules = [
            rule
            for rule in config.get('packageRules', [])
            if rule.get('enabled') is False
        ]
        if strategy == 'actions-github-token':
            # GITHUB_TOKEN cannot push .github/workflows/** changes, so the
            # workflow-file managers must be disabled in this mode.
            managers_disabled = {
                frozenset(rule['matchManagers'])
                for rule in disable_rules
                if 'matchManagers' in rule
            }
            assert frozenset(('github-actions',)) in managers_disabled
            assert any(
                '.github/workflows/**' in rule['matchFileNames']
                for rule in disable_rules
                if 'matchFileNames' in rule
            )
        else:
            # Only the pre-existing docker pinDigest exclusion is disabled.
            assert all(
                rule.get('matchDatasources') == ['docker'] for rule in disable_rules
            )

    check = tmp_path / 'scripts' / 'check-tool-updates.sh'
    assert check.exists()
    assert check.stat().st_mode & stat.S_IXUSR

    answers = (tmp_path / worker.answers_relpath).read_text()
    assert f'tool_update_strategy: {strategy}' in answers
