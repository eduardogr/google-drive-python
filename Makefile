SHELL:=/bin/bash

install:
	pip3 install .

install-dev:
	pip3 install -e '.[dev]'

test:
	pytest $(ARGS)

init-virtual-env:
	./scripts/venv/init.sh

google-auth:
	python3 ./scripts/google/authenticate.py

clean:
	rm -rf build .pytest_cache dist google_drive.egg-info

release:
	./scripts/release/release.sh
