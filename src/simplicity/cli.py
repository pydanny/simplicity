from cookiecutter import main
from rich import print
import typer

app = typer.Typer()


@app.command()
def create():
    main.cookiecutter('https://github.com/pydanny/simplicity.git')


@app.command()
def update():
    print('[bold red]TODO[/bold red]: Updating your package')


if __name__ == "__main__":
    app()
