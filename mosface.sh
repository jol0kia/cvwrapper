#!/bin/bash

if [ $# -eq 1 ]; then
	python3 mosface.py $1
elif [ $# -eq 2 ]; then
	python3 mosface.py $1 $2
else
	echo "usage: $0 [path of input image]"
	echo "usage: $0 [path of input image] [path of output image]"
fi
