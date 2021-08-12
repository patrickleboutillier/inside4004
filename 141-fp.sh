#!/bin/bash

PYTHON=python3
if which pypy3 >/dev/null ; then
    PYTHON=pypy3
fi

$PYTHON 141-fp/mcs4.py 141-fp/ROM.bin
