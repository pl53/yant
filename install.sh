#!/bin/bash
SRC_DIR=/usr/local/yant
BIN_DIR=/usr/local/bin
if [ ! -d "$SRC_DIR" ]; then
   mkdir $SRC_DIR 
fi
cp ./*.py $SRC_DIR 
cp ./yant $BIN_DIR
chmod a+x $SRC_DIR/yant.py
chmod a+x $BIN_DIR/yant
