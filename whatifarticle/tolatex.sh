#!/bin/bash

f="whatifcontent.tex"
[[ -e ${f} ]] && mv ${f} ${f}".bak"
for i in ./*.txt;do
    echo "processing ${i}"
    ./tolatex.py "${i}" ${f}
done
