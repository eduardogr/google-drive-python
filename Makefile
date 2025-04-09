SHELL:=/bin/bash

install:
	poetry install

install-dev:
	pip3 install -e '.[dev]'

test:
	poetry run pytest $(ARGS)

google-auth:
	python3 ./scripts/google/authenticate.py

clean:
	rm -rf build .pytest_cache dist google_drive.egg-info

release:
	./scripts/release/release.sh
