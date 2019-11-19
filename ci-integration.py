#!/usr/bin/env python3
import subprocess as sp;
import os;
import shutil;

sourceFolder = "sonarqube-repair/source/act/TraceSortList";
sp.call('hub clone kth-tcs/sonarqube-repair', shell = True);
sp.call('mvn clean package', shell = True, cwd = "sonarqube-repair");
sp.call('hub clone nharrand/TraceSortList', shell = True);
sp.call('git checkout -b IteratorNextException', shell = True, cwd = "TraceSortList");
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

for f in originalFiles:
    shutil.copy(f, sourceFolder);

sp.call('java -cp target/sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar Main 2272', shell = True, cwd = "sonarqube-repair")
