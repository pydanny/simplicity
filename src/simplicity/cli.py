import pathlib

import typer
from cookiecutter import main
from rich import print

from .legacy import rst_to_json as legacy_rst_to_json


app = typer.Typer()


@app.command()
def create():
    main.cookiecutter("https://github.com/pydanny/simplicity.git")


@app.command()
def update():
    print("[bold red]TODO[/bold red]: Updating your package")


@app.command()
def rst_to_json(path: pathlib.Path):
    """Convert ReStructuredText to JSON"""
    if not path.exists():
        raise typer.BadParameter(f"Path '{path}' does not exist.")
    print(legacy_rst_to_json(path.read_text()))


if __name__ == "__main__":
    app()
