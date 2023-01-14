#!/bin/sh -l

echo "arguments     : $1"
python3 SPDXMerge.py --docpath $1
