#!/usr/bin/python2.7
# reducer.py
import sys

def reduce_function(word, values):
    # Calculate how many times each word was encountered
    return word, sum(values)                        

prev_key = None
values = []

for line in sys.stdin:
    # Parse key and value
    key, value = line.strip().split('\t',1)                                   

     # If key has changed then one can finish processing the previous key
    if key != prev_key and prev_key is not None:
        result_key, result_value = reduce_function(prev_key, values)
        print(result_key + "|" + str(result_value))
        values = []

    prev_key = key
    values.append(int(value))

# Don't forget about the last value!
if prev_key is not None:
    result_key, result_value = reduce_function(prev_key, values)
    print(result_key + "|" + str(result_value)) 

