SHELL:=/bin/bash

install:
	pip3 install .

install-dev:
	pip3 install -e '.[dev]'

test:
	pytest $(ARGS)

init-virtual-env:
	./init-virtual-env.sh

google-auth:
	python3 google_auth.py

clean:
	rm -rf build .pytest_cache dist google_drive.egg-info

release:
	./scripts/release.sh
