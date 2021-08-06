.PHONY: hdl asm chips

test: hdl chips asm

hdl:
	python -m unittest discover -s test/hdl

chips:
	python -m unittest discover -s test/chips

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

calc:
	python 141-fp/mcs4.py 141-fp/ROM.bin

calcp:
	python -m cProfile 141-fp/mcs4.py 141-fp/ROM.bin
