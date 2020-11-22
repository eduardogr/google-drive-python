
install:
	pip install .

install-dev:
	pip install 'nornirnetwork[dev]'

test:
	pytest $(ARGS)

init-virtual-env:
	./init-virtual-env.sh
