#!/bin/bash

find commons-cli/src/. -type f -name "*.java" > java_paths.txt
rm -r sonarqube-repair/source/act/apache
mkdir -p sonarqube-repair/source/act/apache
while read java_file; do
    cp "$java_file" sonarqube-repair/source/act/apache
done <java_paths.txt
cd sonarqube-repair
java -cp target/sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar Main 2111
