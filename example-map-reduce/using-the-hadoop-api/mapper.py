#!/usr/bin/python2.7
# mapper.py
import sys

def map_function(title):
    fields = title.strip().split('\t')         # Split title to fields using the data delimeter
    primaryTitle = fields[2]                   # Select the required field
    for word in primaryTitle.strip().split():  # Split primary title by words
        yield word, 1                          # Use a word as a key

for line in sys.stdin:
    # Call map_function for each line in the input
    for key, value in map_function(line):
        # Emit key-value pairs using '|' as a delimeter  
        print(key + "|" + str(value))
