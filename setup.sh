#!/bin/bash
project=TraceSortList
sourceFolder=sonarqube-repair/source/act/$project
hub clone kth-tcs/sonarqube-repair
cd sonarqube-repair
mvn clean package
cd ..
# hub clone apache/commons-cli
#find commons-cli/src/. -type f -name "*.java" > java_paths.txt
hub clone nharrand/$project
cd $project
git checkout -b BigDecimalDoubleConstructor
find src -type f -name "*.java" > ../java_paths.txt
#rm -r sonarqube-repair/source/act/apache/commons/cli
cd ..
rm -r $sourceFolder
mkdir -p $sourceFolder
while read java_file; do
        cp $project/"$java_file" $sourceFolder
done <java_paths.txt
#rm java_paths.txt
cd sonarqube-repair
java -cp target/sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar Main 2272
find sonarqube-repair/spooned/se -type f -name "*.java" > spooned_files.txt
find TraceSortList/src/main/java/se -type f -name "*.java" && find TraceSortList/src/test/java/se -type f -name "*.java" > original_files.txt
