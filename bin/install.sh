#!/bin/bash
SRC_DIR=/usr/local/yant
BIN_DIR=/usr/local/bin
if [ ! -d "$SRC_DIR" ]; then
   mkdir $SRC_DIR 
fi
cp -r ../yant/ $SRC_DIR/
cp ./yant $BIN_DIR
chmod 755 $SRC_DIR/*.py
chmod 755 $BIN_DIR/yant
echo Finished installation!
echo Now test installation.
../test/system_test.py
