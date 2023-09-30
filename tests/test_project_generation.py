from cookiecutter.main import cookiecutter
import pytest
import shutil
from pathlib import Path
import os
import sys
import subprocess


BASE_DIR = Path(__file__).parent
REPO_DIR = BASE_DIR.parent
NEW_PROJECT_DIR = REPO_DIR / "python_boilerplate"

IMPORTANT_FILES = [
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
]


@pytest.fixture
def context():
    return {
        "full_name": "Daniel Roy Greenfeld",
        "email": "daniel@example.com",
        "github_username": "pydanny",
        "project_name": "Python Boilerplate",
        "slug": "python_boilerplate",
        "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.",
        "command_line_interface": "Yes",
        "version": "0.1.0",
        "license": "MIT",
    }


@pytest.fixture
def generated_project(context):
    cookiecutter(".", no_input=True, extra_context=context)
    yield
    shutil.rmtree(NEW_PROJECT_DIR)


@pytest.mark.usefixtures("generated_project")
def test_project_generation():
    assert NEW_PROJECT_DIR.exists()


@pytest.mark.usefixtures("generated_project")
@pytest.mark.parametrize("important_file", IMPORTANT_FILES)
def test_all_files_generated(important_file):
    assert (NEW_PROJECT_DIR / important_file).exists()


@pytest.mark.usefixtures("generated_project")
def test_no_placeholders_left():
    for foldername, _, filenames in os.walk(NEW_PROJECT_DIR):
        for filename in filenames:
            filepath = Path(foldername) / filename
            with open(filepath, "r") as file:
                content = file.read()
                assert "{{cookiecutter" not in content
                

def test_makefile_works():
    subprocess.run(["make"], check=True, cwd=REPO_DIR)
