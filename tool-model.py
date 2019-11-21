#!/usr/bin/env python3
import os;
import subprocess as sp;
import shutil;
import filecmp;

if(os.environ['TRAVIS_BRANCH'] == 'master' and os.environ['TRAVIS_PULL_REQUEST'] == 'false'):
    project ='Bogus-CI-Integration-Test';
    SQR = 'sonarqube-repair';
    sourceFolder = SQR + '/source/act/' + project;
    # Clone SQ-Repair and package it
    sp.call('git clone git@github.com:kth-tcs/sonarqube-repair.git', shell = True);
    sp.call('mvn clean package', shell = True, cwd = SQR);
    # Clone the project to be analyzed and make a branch
    sp.call('git clone git@github.com:HarisAdzemovic/'+project, shell = True);
    sp.call('git checkout -b IteratorNextException', shell = True, cwd = project);
    # Find all java files in the project to be analyzed
    originalFiles = [];
    for r, d, f in os.walk(project):
        for file in f:
            if '.java' in file:
                originalFiles.append(os.path.join(r, file))

    # Create a directory in SQ-repair to hold the originals
    try:
        shutil.rmtree(sourceFolder, ignore_errors=True);
    except OSError:
        print ('Directory does not exist');
    os.makedirs(sourceFolder);
    for f in originalFiles:
        shutil.copy(f, sourceFolder);
    sp.call('java -cp target/sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar Main 2272', shell = True, cwd = SQR)

    # Go over all Spooned files and compare them to originals. If a diff is found, replace it.
    path = SQR + '/spooned'
    spoonedFiles = [];
    for r, d, f in os.walk(path):
        for file in f:
            if '.java' in file:
                spoonedFiles.append(os.path.join(r, file))

    for o in originalFiles:
        for s in spoonedFiles:
            if(o.split('/')[-1] == s.split('/')[-1]):
                if(not filecmp.cmp(o, s)):
                    shutil.copy(s, o);
                break;

    # Make a commit, fork the project and push the commit
    sp.call('git commit -a -m "Next should call hasNext and throw a NoSuchElementException"', shell = True, cwd = project);
    sp.call('git push origin IteratorNextException', shell = True, cwd = project);
else:
    print("Wrong branch or PR");
