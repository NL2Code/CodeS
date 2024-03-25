# fastapi-code-generator

This code generator creates a FastAPI app from an openapi file.

## This project is in experimental phase.

fastapi-code-generator uses datamodel-code-generator to generate pydantic models

## Installation

To install `fastapi-code-generator`:
```sh
$ pip install fastapi-code-generator
```

## Usage

The `fastapi-code-generator` command:
```
Usage: fastapi-codegen [OPTIONS]

Options:
  -i, --input FILENAME     [required]
  -o, --output PATH        [required]
  -t, --template-dir PATH
  -m, --model-file         Specify generated model file path + name, if not default to models.py
  -r, --generate-routers   Generate modular api with multiple routers using RouterAPI (for bigger applications).
  --specify-tags           Use along with --generate-routers to generate specific routers from given list of tags.
  -c, --custom-visitors    PATH - A custom visitor that adds variables to the template.
  --install-completion     Install completion for the current shell.
  --show-completion        Show completion for the current shell, to copy it
                           or customize the installation.
  --help                   Show this message and exit.
```