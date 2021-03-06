In this tutorial you are going to learn the simple map-reduce functionality using an example. 

Before you read this example you should go through the map reduce excercises in the brightpsace.
One of the excercise is for installing hadoop on ubuntu. Note that you might have to change the hadoop version numbers depending on what is the latest one.
The current version is hadoop-3.1.2.tar.gz.

Once you have the hadoop installed and assuming you have python on your machine, we can look at the examples below.

*Note*: to get these files from this folder just clone the repository to your machine where you have installed hadoop

# Dataset

we use the titles.basic dataset. Read about it at https://www.imdb.com/interfaces/. You can download this dataset from https://datasets.imdbws.com/.
The command is

```
$ wget https://datasets.imdbws.com/title.basics.tsv.gz
$ gunzip title.basics.tsv.gz
$ ls -lh
```

if everything worked you should have a titles.basic.tsv file with approximate 512 MB

# Simple Example

For the first example you will learn to run map reduce as a command line process. This reads a file and count words separated by tabs and spaces.

```
$ cd command-line-example
$ chmod +x *.py
$ cat cmdlinemapper | ./cmdlinemapper.py |sort -t '|' -k1,1 | ./cmdlinereducer.py
```

Note that this reads the file contents -- the cat command -- maps it , sorts and reduces it. You can run this chain in parts -- for example just look at the map output and then sort and then reduce. Open the code and inspect it.


# Bigger Example.

the titles.basic file is tab and pipe separated. hence the simple mapper and reducer code will not work. Hence we use slightly modified code from https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/. Copy the titles.basic.tsv here.

First try to run this with 100 entries from title file

```
$ cd using-the-hadoop-api
$ ls title.basics.tsv
$ chmod +x *.py
$ head -100 title.basics.tsv | ./mapper.py |sort -t '|' -k1,1 | ./reducer.py
```

it should give you the expected output will count of words in title of movies. Now try to run it on all title. instead of head -100 just say cat title.basics.tsv and give the rest of the pipline as input - check if it works and how long it takes.

Now use hadoop for it. Assuming you installed hadoop using the installtion pdf in excercises folder.

```
$ cd using-the-hadoop-api
$ ls title.basics.tsv
$ /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar -input title.basics.tsv -output /home/riaps/map-reduce/output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py 
```

Check the output and compare time

# Finally 

https://github.com/vu-topics-in-big-data-2021/examples/blob/main/example-map-reduce/colab/hadoop.ipynb 

Follow the steps
