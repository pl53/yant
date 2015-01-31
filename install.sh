#!/bin/bash
SRC_DIR=/usr/local/yanote
BIN_DIR=/usr/local/bin
if [ ! -d "$SRC_DIR" ]; then
   mkdir $SRC_DIR 
fi
cp *.py $SRC_DIR 
cp yanote $BIN_DIR
chmod a+x $SRC_DIR/yanote.py
chmod a+x $BIN_DIR/yanote
