from pathlib import Path
import tomllib
import toolspec

EXPECTED_PACKAGE_VERSION = "1.6.1"

def test_release_version_is_consistent():
    root = Path(__file__).resolve().parents[1]
    with (root / "pyproject.toml").open("rb") as f:
        project_version = tomllib.load(f)["project"]["version"]

    assert project_version == EXPECTED_PACKAGE_VERSION
    assert toolspec.__version__ == EXPECTED_PACKAGE_VERSION
    assert project_version == toolspec.__version__
