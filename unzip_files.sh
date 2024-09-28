#!/bin/bash

# Set the directory where your zip files are located
ZIP_DIR=$1

# Change to the specified directory
cd "$ZIP_DIR"

# Unzip all zip files
for zip_file in *.zip; do
    unzip "$zip_file"
done
