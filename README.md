# ToolSpec 1.6.2

ToolSpec is a language-independent contract for self-describing executable JSON tools. This repository contains the Python reference implementation. ToolHub is one possible consumer; MCP adapters can map ToolSpec schemas without making MCP a dependency.

A small Python base package for ToolHub tools.

## ToolSpec

A tool subclasses `Tool`, declares Pydantic `input_model` / `output_model`,
`description`, `requirements`, `few_shots`, and implements `biz()`.

For dependency-independent discovery, invoke the tool through a tiny launcher:

```python
from pathlib import Path
from toolspec.bootstrap import run_tool_file

run_tool_file(Path(__file__).with_name("tool.py"))
```

The example is in `examples/list_directory`.

## INPUT_DESCRIBE

When `INPUT_DESCRIBE` is non-empty, describe output always goes to stdout.
Normal `output.json` handling is bypassed.

Supported values:

- `brief` — textual description.
- `schema` — `input_schema` and `output_schema`.
- `few_shots` — retained for 0.1.x compatibility.
- `requirements` — `{tool, format, content}`.
- `json_spec` — `{description, requirements, input_schema, output_schema, few_shots}`.

`requirements` is extracted without importing the tool module.

For `json_spec`, if importing/executing the tool fails with `ImportError` or
`ModuleNotFoundError`, static fields are still returned and both schemas are
`{}`.

Example:

```bash
INPUT_DESCRIBE=requirements python examples/list_directory/run.py
INPUT_DESCRIBE=json_spec python examples/list_directory/run.py
```

## Build

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip build
python -m pip install -e '.[test]'
pytest
python -m build
```

Install the resulting wheel:

```bash
python -m pip install dist/toolspec-0.5.0-py3-none-any.whl
```

## Architecture decisions

See `docs/adr/0002-static-describe-bootstrap.md`.

## Regression policy

Tests are cumulative across releases. See `docs/adr/0003-cumulative-regression-tests.md`.

## Release verification

Run `python -m pytest -q` and then `python scripts/verify_package.py`. Both must pass before release.

## CLI/stdin transport

Examples:

```bash
python tool.py '{"path":"."}'
printf '%s' '{"path":"."}' | python tool.py
python tool.py '{"describe":"json_spec"}'
```

CLI/stdin results go to stdout. With non-empty `describe`, business input is not Pydantic-validated; only the describe mode is validated. `json_spec` includes `format_version: "1.0"`.


## Tool identity and service CLI options

A concrete tool declares its own identity:

```python
class MyTool(Tool[Input, Output]):
    name = "my-tool"
    version = "1.0.0"
```

`name` and `version` are included in `json_spec` only. Service options are
processed before all input transports and validation:

```bash
python tool.py --help
python tool.py -h
python tool.py --version
python tool.py -v
```

## ToolSpec

See `TOOLSPEC.md`. ToolSpec 1.1 uses MCP-aligned `inputSchema` and `outputSchema`; MCP itself is not a dependency. Python code continues to use `input_model` and `output_model`.

## Schema contract identity

ToolSpec 1.3 supports independent schema contracts:

```python
class MyTool(Tool[Input, Output]):
    input_schema_name = "MyToolInput"
    input_schema_version = "1.0.0"
    output_schema_name = "MyToolOutput"
    output_schema_version = "1.0.0"
```

They are emitted as JSON Schema `$id` and `x-schema-version`.

## Strict object contracts

ToolSpec 1.4 rejects undeclared fields recursively on both input and output. Generated JSON Schema mirrors runtime validation with `additionalProperties: false`.

## Validation diagnostics

ToolSpec 1.5 emits concise validation diagnostics on stderr. Use `--debug` or `TOOLSPEC_DEBUG=1` for validation tracebacks. Input/output validation failures use exit statuses 2/3.

## Error format

Use `--error-format human|json` or `TOOLSPEC_ERROR_FORMAT=human|json`. CLI overrides the environment; `human` is the default. JSON + debug keeps stderr valid JSON by placing the traceback in `error.traceback`.

## Error origin

JSON is the default error format. `source=toolspec` identifies framework/protocol failures; `source=tool`, `stage=biz` identifies business-function failures. Select `--error-format human` for human/native behavior.
