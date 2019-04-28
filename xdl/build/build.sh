#!/bin/sh

cmake .. -DTF_BACKEND=1
if [ $? -ne 0 ]; then
  echo "cmake with backend failed"
fi

make -j32
if [ $? -ne 0 ]; then
  echo "make failed"
fi

make install_python_lib
if [ $? -ne 0 ]; then
  echo "make install python lib failed"
fi

python -c "import xdl; print xdl.__version__"
if [ $? -ne 0 ]; then
  echo "test xdl failed"
fi

