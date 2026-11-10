__author__ = "{{ cookiecutter.full_name | replace('\\', '\\\\') | replace('"', '\\"') }}"
__email__ = "{{ cookiecutter.email | replace('\\', '\\\\') | replace('"', '\\"') }}"


def main():
    return "Hello, world!"
