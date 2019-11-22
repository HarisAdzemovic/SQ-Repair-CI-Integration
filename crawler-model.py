#!/usr/bin/env python3

## A prototype for what a CI integration of Sonarqube-repair could look like.
## Inspired by Repairnator, it would crawl the web for suitable projects, apply
## its code transformations/processors and create ready pull requests
import subprocess as sp;
import os;
import shutil;
import filecmp;
import sys;

project = sys.argv[1];
projectOwner = sys.argv[2];
rules = ['2111', '2116', '2272', '4973'];
SQR = 'sonarqube-repair';
branch = 'SonarqubeRepair';
sourceFolder = 'source/act/' + project;

# Clone the project to be analyzed and make a branch
sp.call(['hub', 'clone', projectOwner + '/' + project]);
sp.call(['git', 'checkout', '-b', branch], cwd = project);

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

for rule in rules:
    for f in originalFiles:
        shutil.copy(f, sourceFolder);

    # Perform transformation on all files
    sp.call(['java', '-cp', 'sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar', 'Main', rule])

    # Go over all Spooned files and compare them to originals. If a diff is found, replace it.
    path = 'spooned'
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
sp.call(['git', 'commit', '-a', '-m', 'Repairs Sonarqube violations'], cwd = project);
sp.call(['hub', 'fork', '--remote-name=origin'], cwd = project);
sp.call(['git', 'push', 'origin', branch], cwd = project);

# Clean up
sp.call(['rm', '-rf', 'source']);
sp.call(['rm', '-rf', 'spooned']);
sp.call(['rm', '-rf', project]);
