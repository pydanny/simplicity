.DEFAULT_GOAL := help # Sets default action to be help

define PRINT_HELP_PYSCRIPT # start of Python section
import re, sys

output = []
# Loop through the lines in this file
for line in sys.stdin:
	# if the line has a command and a comment start with
	#   two pound signs, add it to the output
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		output.append("%-10s %s" % (target, help))
# Sort the output in alphanumeric order
output.sort()
# Print the help result
print('\n'.join(output))
endef
export PRINT_HELP_PYSCRIPT # End of python section

GH_CLI := $(shell command -v gh 2> /dev/null)

ghcheck:  ## Check if GH CLI is installed
ifndef GH_CLI
	$(error "GitHub CLI (gh) not found on PATH. See https://cli.github.com/ to install.")
endif

help:  ## Print the help text
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

changelog: ghcheck ## Fetches the changelog from the release. Requires GH CLI and correct token access permissions
	gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/{{cookiecutter.slug}}/releases/latest > changelog.json
	python utils/update_changelog.py
	rm changelog.json

lint:  ## Lint all the Python code
	black .
	ruff check . --fix

VERSION=v$(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

tag:  ## Tag the project for release
	echo "Tagging version $(VERSION)"
	git tag -a $(VERSION) -m "Creating version $(VERSION)"
	git push origin $(VERSION)


test:  ## Run the tests
	coverage run -m pytest .
	coverage report -m
	coverage html
