test:
	@for t in tests/[0-9]*.py ; do echo -n "$$t: " ; \
		python $$t > /tmp/asm ; \
		python mcs4.py /tmp/asm > /tmp/out 2>&1 ; \
		if [ "$$?" = 0 ] ; then \
			echo OK ; \
		else \
			echo "NOK!" ; \
			cat /tmp/out ; \
			exit 1 ; \
		fi ; \
	done

