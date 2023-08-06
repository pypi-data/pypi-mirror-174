build-docs:
	sphinx-build -v -b coverage docs/source docs/build/coverage
	cd docs; make html

build:
	pytest
	hatch run lint
	hatch run sort
	pre-commit run --all-files
	hatch run cov

build-push:
	pytest
	hatch run lint
	hatch run sort
	pre-commit autoupdate
	pre-commit install
	pre-commit run --all-files

all: build-docs build