"""The child consumes the shared workflow dependency contract."""

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_shared_workflow_plugin_is_refreshed_before_install() -> None:
    """A declaration must not be the only record of the shared workflow source."""
    manifest = tomllib.loads((ROOT / 'agents.toml').read_text())
    assert manifest['plugins'] == [
        {'name': 'mattpocock-skills', 'source': 'mattpocock/skills'}
    ]
    tasks = tomllib.loads((ROOT / 'mise.toml').read_text())['tasks']
    refresh = tasks['dotagents-add']['run']
    assert refresh.index('add mattpocock/skills --all') < refresh.index(
        '--project install'
    )
    assert tasks['dotagents-install']['run'] == 'dotagents --project install'
