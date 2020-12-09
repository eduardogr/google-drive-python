
install:
	pip3 install .

install-dev:
	pip3 install '.[dev]'

test:
	pytest $(ARGS)

init-virtual-env:
	./init-virtual-env.sh
