from pathlib import Path
from toolspec.bootstrap import run_tool_file

run_tool_file(Path(__file__).with_name("tool.py"))
