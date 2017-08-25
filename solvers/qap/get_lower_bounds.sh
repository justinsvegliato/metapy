#!/bin/bash
for filename in /Users/justinsvegliato/Documents/Development/metapy/problems/200-qap/*.dat; do
    echo "$filename"
    ./qapglb < $filename
done