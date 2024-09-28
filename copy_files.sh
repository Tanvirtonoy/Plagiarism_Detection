#!/bin/bash

name=$1
zip=1
if [ $zip == $2 ]
then
    project=project5/project5*
else
    project=project5
fi
cp $project/src/main/scala/Graph.scala Plagiarism/scala/$name.txt
cp $project/graph.distr.out Plagiarism/distr/$name.txt
