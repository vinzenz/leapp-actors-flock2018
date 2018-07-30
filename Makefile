get_upstream:
	git clone https://github.com/leapp-to/leapp-actors
	cp -a repos-internal leapp-actors/repos

install-deps:
	make get_upstream; \
	cd leapp-actors; \
	make install-deps

test:
	cd leapp-actors; \
	make test

fastsrpm:
	LEAPP_INITRD_SKIP=1 scripts/build-srpm.sh

srpm:
	scripts/build-srpm.sh

clean:
	rm -rf leapp-actors
	rm -rf build/ dist/ *.egg-info
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

.PHONY: get_upstream install-deps test clean srpm
