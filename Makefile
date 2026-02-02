MANAGE = ./manage.py
LANGUAGES:=`find ./locale/ -mindepth 1 -maxdepth 1 -type d -printf "--locale %f "`

npm:
	test -d node_modules || npm install

test: npm
	python -m pytest

setup: npm
	uv sync --no-sources

#coverage:
#	coverage run -m pytest

check:
	uv run ruff check src

doc:
	mkdocs build -d docs/build/doc/

doc-dev:
	mkdocs serve -a localhost:8002

build-js:
	scripts/build_js.sh

build: npm build-js
	# remove dist/ if it exists
	rm -rf dist/
	uv build

# https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi
publish:
	scripts/publish.sh

tetrabuild:
	uv run $(MANAGE) tetrabuild

collectstatic:
	uv run $(MANAGE) collectstatic --noinput

deploy: localecompile tetrabuild collectstatic

localegen:
    # don't --keep-pot
	uv run $(MANAGE) makemessages --ignore "static/*"  --ignore "build/*" $(LANGUAGES)
	uv run $(MANAGE) makemessages -d djangojs --ignore "static/*" --ignore "build/*" --ignore "node_modules/*" $(LANGUAGES)

localecompile:
	uv run $(MANAGE) compilemessages --ignore ".venv"

locale: localegen localecompile
