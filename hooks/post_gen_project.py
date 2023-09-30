from pathlib import Path


def remove_cli():
    """Remove the cli.py file."""
    cli_path = Path("src/{{cookiecutter.slug}}/cli.py")
    cli_path.unlink()


def main():
    if "{{ cookiecutter.command_line_interface }}" == "No":
        remove_cli()


if __name__ == "__main__":
    main()
