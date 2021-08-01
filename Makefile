.PHONY: hdl asm

test: hdl asm

hdl:
	python -m unittest discover -s test/hdl

asm:
	@for t in test/asm/[0-9]*.py ; do echo -n "$$t: " ; \
		python $$t > /tmp/asm ; \
		python test/mcs4.py /tmp/asm > /tmp/out 2>&1 ; \
		if [ "$$?" = 0 ] ; then \
			echo OK ; \
		else \
			echo "NOK!" ; \
			cat /tmp/out ; \
			exit 1 ; \
		fi ; \
	done

