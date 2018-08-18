#!/bin/bash
nohup python -m lib.extract_words > extract-words.txt  2>&1 &
tail -f extract-words.txt -n 100
