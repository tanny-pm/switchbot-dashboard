# pyproject-template

Python project template using poetry.

## Installation

1. Install poetry

https://cocoatomo.github.io/poetry-ja/

2. Install dependencies

```
$ poetry install
```

## Basic usage

Install the package and sub-dependencies.

```
$ poetry add pendulum
$ poetry add -D pytest
```

To run your script simply use `poetry run python your_script.py`.

```
$ poetry run pytest
```

```
$ poetry run python -m pyproject_template
```

## Commands

If you want to exclude one or more dependency groups for the installation, you can use the `--without` option.

```
$ poetry install --without dev
```

In order to get the latest versions of the dependencies and to update the `poetry.lock` file, you should use the `update` command.

```
$ poetry update
```

The `remove` command removes a package from the current list of installed packages.

```
$ poetry remove pendulum
```

This command exports the lock file to other formats.

```
$ poetry export -f requirements.txt --output requirements.txt
```

## References

- https://python-poetry.org/
