import shutil
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter
from setuptools.config.pyprojecttoml import read_configuration


REPO_DIR = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "description",
    [
        "A package for processing text.",
        'A parser for "quoted" text.',
        r"Read files from C:\Users\Public.",
        r"Read files from C:\new\reports.",
        'Keep the sequence \\" intact.',
        "A user's 日本語 package 📦.",
    ],
)
def test_generated_package_preserves_description(tmp_path, description):
    """The build backend must read the description exactly as entered."""
    # Isolate package metadata from unrelated workflow templates and hooks.
    template = tmp_path / "template"
    project_template = template / "{{cookiecutter.slug}}"
    project_template.mkdir(parents=True)
    shutil.copyfile(REPO_DIR / "cookiecutter.json", template / "cookiecutter.json")
    shutil.copyfile(
        REPO_DIR / "{{cookiecutter.slug}}" / "pyproject.toml",
        project_template / "pyproject.toml",
    )
    project = Path(
        cookiecutter(
            str(template),
            no_input=True,
            output_dir=str(tmp_path / "output"),
            default_config={"replay_dir": str(tmp_path / "replay")},
            extra_context={"project_short_description": description},
        )
    )
    configuration = read_configuration(str(project / "pyproject.toml"), expand=False)
    assert configuration["project"]["description"] == description
