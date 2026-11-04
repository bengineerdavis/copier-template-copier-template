"""Tests for vcs_platform feature."""

from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    ('sub_project', 'expect_gitlab', 'expect_github'),
    [
        ({'vcs_platform': 'gitlab'}, True, False),
        ({'vcs_platform': 'github'}, False, True),
        ({'vcs_platform': ''}, False, False),
    ],
    indirect=['sub_project'],
)
def test_vcs_platform_files(
    sub_project: Path, expect_gitlab: bool, expect_github: bool
) -> None:
    """Test that VCS platform files are included based on vcs_platform."""
    assert (sub_project / '.gitlab-ci.yml').exists() == expect_gitlab
    assert (sub_project / '.gitlab').is_dir() == expect_gitlab
    assert (
        sub_project / '.github' / 'workflows' / 'test.yml'
    ).exists() == expect_github
    assert (sub_project / '.github').is_dir() == expect_github


@pytest.mark.parametrize(
    ('sub_project', 'answers_have_strategy'),
    [
        ({'vcs_platform': 'gitlab'}, False),
        ({'vcs_platform': 'github'}, True),
        ({'vcs_platform': ''}, False),
    ],
    indirect=['sub_project'],
)
def test_tool_update_strategy_gated_on_platform(
    sub_project: Path, answers_have_strategy: bool
) -> None:
    """The Actions-based strategies only make sense on GitHub.

    Off-github the strategy question is not asked (the `when` gate), so no
    tool-update artifacts are stamped and the answers file records no
    strategy — a regression removing the gate would re-expose the
    impossible combination of an actions strategy with no workflow.
    """
    answers = (sub_project / '.copier-answers.copier-template.yml').read_text()
    assert ('tool_update_strategy:' in answers) is answers_have_strategy

    renovate_json = sub_project / 'renovate.json'
    assert renovate_json.exists() is answers_have_strategy
    if answers_have_strategy:
        json.loads(renovate_json.read_text())

    # The github default strategy is github-app, which stamps no workflow.
    assert not (sub_project / '.github' / 'workflows' / 'renovate.yml').exists()
    # The check script has no platform guard; it is stamped unconditionally.
    assert (sub_project / 'scripts' / 'check-tool-updates.sh').exists()
