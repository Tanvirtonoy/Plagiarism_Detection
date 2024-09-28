#!/bin/bash

project=project5
rm -rf $project*
zip=0
if [ $1 == $zip ]
then
    fname="$(find /mnt/c/Users/Tanvir/Downloads/*.zip -mmin -5)"
    mv $fname ./$project.zip
    unzip $project.zip -d $project
else
    fname="$(find /mnt/c/Users/Tanvir/Downloads/*.tgz -mmin -5)"
    mv "$fname" ./$project.tgz
    mkdir $project
    tar xfz $project.tgz -C $project
fi
code $project
