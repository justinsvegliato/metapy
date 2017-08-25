#!/bin/bash
for filename in /Users/justinsvegliato/Documents/Development/metapy/problems/200-qap/*.dat; do
    ./qapsim < $filename | grep "~" | sed 's/\~/ /g' > "$filename.results"
done