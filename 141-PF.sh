#!/bin/bash

PYTHON=python3
if which pypy3 >/dev/null ; then
    PYTHON=pypy3
fi

cat 141-PF/ROM.bin | $PYTHON 141-PF/mcs4.py
