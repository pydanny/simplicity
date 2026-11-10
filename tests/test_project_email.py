import importlib.util
import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from setuptools.config.pyprojecttoml import read_configuration


REPO_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(
    params=[
        pytest.param("alex@example.org", id="ordinary"),
        pytest.param('"alex morgan"@example.org', id="quoted-space"),
        pytest.param(r'"alex\\morgan"@example.org', id="quoted-backslash"),
    ]
)
def generated_email(tmp_path, request):
    # Render the actual metadata/module templates apart from unrelated workflows.
    template = tmp_path / "template"
    project_template = template / "{{cookiecutter.slug}}"
    module_path = Path("src") / "{{cookiecutter.slug}}" / "__init__.py"
    (project_template / module_path).parent.mkdir(parents=True)
    shutil.copyfile(REPO_DIR / "cookiecutter.json", template / "cookiecutter.json")
    for path in [Path("pyproject.toml"), module_path]:
        shutil.copyfile(
            REPO_DIR / "{{cookiecutter.slug}}" / path, project_template / path
        )
    project = Path(
        cookiecutter(
            str(template),
            no_input=True,
            output_dir=str(tmp_path / "output"),
            default_config={"replay_dir": str(tmp_path / "replay")},
            extra_context={"full_name": "Alex Morgan", "email": request.param},
        )
    )
    return project, request.param


def test_generated_metadata_preserves_email(generated_email):
    project, email = generated_email
    configuration = read_configuration(str(project / "pyproject.toml"), expand=False)
    for role in ["authors", "maintainers"]:
        assert configuration["project"][role] == [
            {"name": "Alex Morgan", "email": email}
        ]


def test_generated_module_preserves_email(generated_email):
    project, email = generated_email
    spec = importlib.util.spec_from_file_location(
        "generated_email_package",
        project / "src" / "python_boilerplate" / "__init__.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.__author__ == "Alex Morgan"
    assert module.__email__ == email
    assert module.main() == "Hello, world!"
