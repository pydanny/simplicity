import os
import subprocess
import sys
from pathlib import Path
import pytest
import shutil
from cookiecutter.main import cookiecutter


# Define constants
BASE_DIR = Path(__file__).parent
REPO_DIR = BASE_DIR.parent
NEW_PROJECT_DIR = REPO_DIR / "python_boilerplate"

IMPORTANT_FILES = [
    # List of all important files in the project
    "pyproject.toml",
    "Makefile",
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "utils/update_changelog.py",
    "tests/__init__.py",
    "tests/test_python_boilerplate.py",
    ".github/workflows/python-ci.yml",
    ".github/workflows/python-publish.yml",
    "docs/releasing.md",
    "src/python_boilerplate/__init__.py",
]


# Fixtures
@pytest.fixture
def context():
    """Returns the context dictionary used for project generation."""
    return {
        "full_name": "Daniel Roy Greenfeld",
        "email": "daniel@example.com",
        "github_username": "pydanny",
        "project_name": "Python Boilerplate",
        "slug": "python_boilerplate",
        "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.",
        "command_line_interface": "No",
        "version": "0.1.0",
        "license": "MIT",
    }


@pytest.fixture
def generated_project(context):
    """Generates a project using cookiecutter and cleans up after the test is done."""
    cookiecutter(".", no_input=True, extra_context=context)
    yield
    shutil.rmtree(NEW_PROJECT_DIR)


# Tests
@pytest.mark.usefixtures("generated_project")
def test_project_generation():
    """Tests if the project is generated successfully."""
    assert NEW_PROJECT_DIR.exists()


@pytest.mark.usefixtures("generated_project")
@pytest.mark.parametrize("important_file", IMPORTANT_FILES)
def test_all_files_generated(important_file):
    """Tests if all important files are generated."""
    assert (NEW_PROJECT_DIR / important_file).exists()


@pytest.mark.usefixtures("generated_project")
def test_no_placeholders_left():
    """Tests if there are no placeholders left in the generated project."""
    for foldername, _, filenames in os.walk(NEW_PROJECT_DIR):
        for filename in filenames:
            filepath = Path(foldername) / filename
            with open(filepath, "r") as file:
                content = file.read()
                assert "{{cookiecutter" not in content


@pytest.mark.usefixtures("generated_project")
def test_generated_makefile_works():
    """Tests if the generated Makefile works correctly."""
    subprocess.run(["make"], check=True, cwd=NEW_PROJECT_DIR)


def test_cli_is_generated(context):
    """Tests if the CLI is generated correctly when the command_line_interface option is set to Yes."""
    context.update({"command_line_interface": "Yes"})
    cookiecutter(".", no_input=True, extra_context=context)
    assert (NEW_PROJECT_DIR / "src/python_boilerplate/cli.py").exists()
    shutil.rmtree(NEW_PROJECT_DIR)
