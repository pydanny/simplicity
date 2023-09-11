# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

## Features

- TODO

## Installation

```bash
pip install {{cookiecutter.slug}}
```

### Usage: How {{cookiecutter.slug}} handles initial arguments

TODO

## Development

Install dev dependencies:

```
pip install -r requirements-dev.txt
```

Install the package in editable mode:

```bash
pip install -e .
```

### Code quality

```bash 
make lint
```

### Testing

```bash
make test
```

### Releasing on PyPI

1. Update the `version` in `pyproject.toml`. We use semantic versioning
2. At the command line, run `make tag`
3. Go to [tags page](https://github.com/{{cookiecutter.__gh_slug}}/tags), choose the most recent tag, and click `Draft a new release`


### Building the project locally

Go to the project root

```bash
pip install --upgrade build
python -m build
```

Test the project, forcing reinstall if necessary

```bash
pip install dist/*.whl --force-reinstall
```

# Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [cookiecutter-pymodule](https://github.com/pydanny/cookiecutter-pymodule) project template.
