#!/bin/bash

for i in ./*.txt;do
    echo "processing ${i}"
    ./tolatex.py "${i}" >> whatif.txt
done
