```
cat file1.txt | ./cmdlinemapper.py |sort -t '|' -k1,1 | ./cmdlinereducer.py
```