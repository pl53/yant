#!/bin/bash

DIR=/usr/local/
cp -r ../yant $DIR/
cp ./yant $DIR/bin/
chmod 755 $DIR/yant/runner.py
chmod 755 $DIR/bin/yant
echo Finished installation!
