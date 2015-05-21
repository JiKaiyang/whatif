#!/bin/bash

[[ -e whatif.tex ]] && mv whatif.tex whatif.tex.bak
for i in ./*.txt;do
    echo "processing ${i}"
    ./tolatex.py "${i}" >> whatif.tex
done
