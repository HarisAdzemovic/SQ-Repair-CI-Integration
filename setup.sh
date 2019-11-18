#!/bin/bash
hub clone kth-tcs/sonarqube-repair
cd sonarqube-repair
mvn clean package
cd ..
hub clone apache/commons-cli
