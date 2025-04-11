SHELL:=/bin/bash

check:
	poetry check

install:
	poetry install

install-dev:
	poetry install --with dev

test:
	poetry run pytest $(ARGS)

build:
	poetry build

publish-locally:
	eval $(shell poetry env activate) && python3 -m pip install dist/googledrive-*.tar.gz

publish:
	poetry publish --dry-run

release:
	./scripts/release/release.sh

clean:
	rm -rf build .pytest_cache dist google_drive.egg-info