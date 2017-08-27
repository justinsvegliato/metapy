#!/bin/bash
for filename in /Users/justinsvegliato/Documents/Development/metapy/problems/10-10-50-jsp/*.txt; do
    python2.7 jsp-ga.py $filename > "$filename.results"
done