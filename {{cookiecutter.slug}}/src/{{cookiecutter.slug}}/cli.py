import typer
from rich import print


app = typer.Typer()


@app.command()
def hello():
    print("[green]Hello, world![/green]")


@app.command()
def todo():
    print("[bold red]TODO[/bold red]: Add another command here")


if __name__ == "__main__":
    app()
