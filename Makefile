MANAGE = ./manage.py
LANGUAGES:=`find ./locale/ -mindepth 1 -maxdepth 1 -type d -printf "--locale %f "`

npm:
	test -d node_modules || npm install

test: npm
	python -m pytest

#coverage:
#	coverage run -m pytest

check:
	ruff check src

doc:
	mkdocs build -d docs/build/doc/

doc-dev:
	mkdocs serve -a localhost:8002

build-js:
	scripts/build_js.sh

build: npm build-js
	# remove dist/ if it exists
	rm -rf dist/
	python -m build

# https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi
publish:
	scripts/publish.sh

tetrabuild:
	$(MANAGE) tetrabuild

collectstatic:
	$(MANAGE) collectstatic --noinput

deploy: localecompile tetrabuild collectstatic

localegen:
    # don't --keep-pot
	$(MANAGE) makemessages --ignore "static/*"  --ignore "build/*" $(LANGUAGES)
	$(MANAGE) makemessages -d djangojs --ignore "static/*" --ignore "build/*" $(LANGUAGES)

localecompile:
	$(MANAGE) compilemessages

locale: localegen localecompile
