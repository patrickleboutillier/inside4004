#!/bin/bash

PYTHON=python3
if which pypy3 >/dev/null ; then
    PYTHON=pypy3
fi
if [ -n "$PROFILE" ] ; then
    PYTHON="$PYTHON -m cProfile"
fi

$PYTHON 141-PF/mcs4.py "$@" 141-PF/ROM.bin
