#!/usr/bin/env python3
import subprocess;
import os;
import shutil;

sourceFolder = "sonarqube-repair/source/act/TraceSortList";
subprocess.call('hub clone kth-tcs/sonarqube-repair', shell = True);
subprocess.call('mvn clean package', shell = True, cwd = "sonarqube-repair");
subprocess.call('hub clone nharrand/TraceSortList', shell = True);
subprocess.call('git checkout -b IteratorNextException', shell = True, cwd = "TraceSortList");
path = "TraceSortList"
originalFiles = [];
for r, d, f in os.walk(path):
    for file in f:
        if '.java' in file:
            originalFiles.append(os.path.join(r, file))

for f in originalFiles:
    print(f)

try:
	shutil.rmtree(sourceFolder, ignore_errors=True);
except OSError:
	print ("Directory does not exist");
os.makedirs(sourceFolder);
