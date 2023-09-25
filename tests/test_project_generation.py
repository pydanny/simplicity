from cookiecutter.main import cookiecutter
import pytest
import os
from pathlib import Path

CURRENT_DIR = Path(__file__)
REPO_DIR = CURRENT_DIR / ".."
NEW_PROJECT_DIR = REPO_DIR / "python_boilerplate/"


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
    

def teardown_function(function):
    """teardown any state that was previously setup with a setup_function
    call.
    """
    os.rmdir(NEW_PROJECT_DIR)
    
    
def test_project_generation(context):
    """Test that project is generated and fully rendered."""

    cookiecutter(
        ".", no_input=True, extra_context=context
    )
    