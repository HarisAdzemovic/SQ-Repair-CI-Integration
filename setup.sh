#!/bin/bash
hub clone kth-tcs/sonarqube-repair
mvn package -f sonarqube-repair/pom.xml
