#!/bin/sh

cmake .. -DTF_BACKEND=1
make -j32

make install_python_lib

