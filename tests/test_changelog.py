import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]


class ChangelogEndpointTests(unittest.TestCase):
    def assert_changelog_endpoint(self, project_dir, expected_endpoint):
        result = subprocess.run(
            ["make", "--just-print", "changelog", "GH_CLI=test-gh"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn(expected_endpoint, shlex.split(result.stdout))

    def test_repository_changelog_uses_owner_and_repository(self):
        self.assert_changelog_endpoint(
            REPO_DIR, "/repos/pydanny/simplicity/releases/latest"
        )

    def test_generated_changelog_uses_configured_owner_and_repository(self):
        from cookiecutter.main import cookiecutter

        for owner, slug in [
            ("example-org", "custom_library"),
            ("another-user", "different_package"),
        ]:
            with self.subTest(owner=owner, slug=slug), tempfile.TemporaryDirectory() as tmp:
                project_dir = cookiecutter(
                    str(REPO_DIR),
                    no_input=True,
                    output_dir=tmp,
                    extra_context={"github_username": owner, "slug": slug},
                )
                self.assert_changelog_endpoint(
                    project_dir, f"/repos/{owner}/{slug}/releases/latest"
                )


if __name__ == "__main__":
    unittest.main()
