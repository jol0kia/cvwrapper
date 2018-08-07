#!/bin/bash

if [ $# -eq 1 ]; then
	python3 mosface.py --sfile $1
elif [ $# -eq 2 ]; then
	python3 mosface.py --sfile $1 --dfile $2
elif [ $# -eq 3 ]; then
	python3 mosface.py --sfile $1 --dfile $2 --brot $3
elif [ $# -eq 4 ]; then
	python3 mosface.py --sfile $1 --dfile $2 --brot $3 --arot $4
else
	echo "usage: $0 [path of input image]"
	echo "usage: $0 [path of input image] [path of output image]"
	echo "usage: $0 [path of input image] [path of output image] [rotation-degree before processing]"
	echo "usage: $0 [path of input image] [path of output image] [rotation-degree before processing] [rotation-degree after processing]"
fi
