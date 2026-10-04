#!/bin/bash
# Mapper script for Hadoop Streaming MapReduce Word Count
while read line
do
  for word in $line
  do
    echo -e "$word\t1"
  done
done
