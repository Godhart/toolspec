from pathlib import Path
import tomllib

ROOT = Path(__file__).parents[1]

def test_hatch_wheel_explicit_package():
    d = tomllib.loads((ROOT/"pyproject.toml").read_text())
    assert d["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"] == ["src/toolspec"]

def test_package_exists():
    assert (ROOT/"src/toolspec/__init__.py").is_file()
