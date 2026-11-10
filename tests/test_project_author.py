import importlib.util
import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from setuptools.config.pyprojecttoml import read_configuration


REPO_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(
    params=[
        "Alex Morgan",
        'Alex "AJ" Morgan',
        "Alex O'Neill",
        "山田 太郎 🧪",
        r"Research\tools",
    ]
)
def generated_author(tmp_path, request):
    # Isolate the actual metadata and module templates from unrelated workflows.
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
            extra_context={"full_name": request.param},
        )
    )
    return project, request.param


def test_generated_metadata_preserves_author(generated_author):
    project, full_name = generated_author
    configuration = read_configuration(str(project / "pyproject.toml"), expand=False)
    for role in ["authors", "maintainers"]:
        assert configuration["project"][role] == [
            {"name": full_name, "email": "daniel@example.com"}
        ]


def test_generated_module_preserves_author(generated_author):
    project, full_name = generated_author
    spec = importlib.util.spec_from_file_location(
        "generated_package", project / "src" / "python_boilerplate" / "__init__.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.__author__ == full_name
    assert module.__email__ == "daniel@example.com"
    assert module.main() == "Hello, world!"
