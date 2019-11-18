#!/bin/bash

find pdfbox/pdfbox/src/. -type f -name "*.java" > java_paths.txt
rm -r sonarqube-repair/source/act/ABC
mkdir -p sonarqube-repair/source/act/ABC
while read java_file; do
    cp "$java_file" sonarqube-repair/source/act/ABC
done <java_paths.txt
