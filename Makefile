SHELL := /bin/bash
PYTHON = $(shell if which pypy3 >/dev/null ; then echo pypy3 ; else echo python3 ; fi)

.PHONY: hdl asm chips

test: hdl chips asm calc

hdl:
	$(PYTHON) -m unittest discover -s test/hdl

chips:
	$(PYTHON) -m unittest discover -s test/chips

asm:
	@for t in test/asm/[0-9]*.py ; do echo -n "$$t: " ; \
		$(PYTHON) $$t > /tmp/rom ; \
		$(PYTHON) test/mcs4.py /tmp/rom > /tmp/out 2>&1 ; \
		if [ "$$?" = 0 ] ; then \
			echo OK ; \
		else \
			echo "NOK!" ; \
			cat /tmp/out ; \
			exit 1 ; \
		fi ; \
	done

calc:
	@for t in test/141-PF/[0-9]*.calc ; do echo -n "$$t: " ; \
		. $$t ; \
		GOT=$$(./141-PF.sh -o | grep '\*' | tail -n1) ; \
		if [ "$$GOT" == "$$EXPECTED" ] ; then \
			echo OK ; \
		else \
			echo "NOK!" ; \
			echo "  '$$GOT'" ; \
			echo "  !=" ; \
			echo "  '$$EXPECTED'" ; \
			exit 1 ; \
		fi ; \
	done

profile:
	@PROFILE=1 ./141-PF.sh
