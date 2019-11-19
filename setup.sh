#!/bin/bash
#hub clone kth-tcs/sonarqube-repair
#cd sonarqube-repair
#mvn clean package
#cd ..
# hub clone apache/commons-cli
#find commons-cli/src/. -type f -name "*.java" > java_paths.txt
hub clone nharrand/TraceSortList
cd TraceSortList
git checkout -b BigDecimalDoubleConstructor
find src -type f -name "*.java" > java_paths.txt
mv java_paths.txt ../
#rm -r sonarqube-repair/source/act/apache/commons/cli
cd ..
rm -r sonarqube-repair/source/act/TraceSortList
mkdir -p sonarqube-repair/source/act/TraceSortList
while read java_file; do
        cp TraceSortList/"$java_file" sonarqube-repair/source/act/TraceSortList
done <java_paths.txt
#rm java_paths.txt
cd sonarqube-repair
java -cp target/sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar Main 2272
