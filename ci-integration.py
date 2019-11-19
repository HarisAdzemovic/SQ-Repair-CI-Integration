#!/usr/bin/env python3
import subprocess as sp;
import os;
import shutil;
import filecmp;

project='TraceSortList';
sourceFolder = 'sonarqube-repair/source/act/' + project;
sp.call('hub clone kth-tcs/sonarqube-repair', shell = True);
sp.call('mvn clean package', shell = True, cwd = 'sonarqube-repair');
sp.call('hub clone nharrand/'+project, shell = True);
sp.call('git checkout -b IteratorNextException', shell = True, cwd = project);
originalFiles = [];
for r, d, f in os.walk(project):
    for file in f:
        if '.java' in file:
            originalFiles.append(os.path.join(r, file))

for f in originalFiles:
    print(f)

try:
    shutil.rmtree(sourceFolder, ignore_errors=True);
except OSError:
    print ('Directory does not exist');
os.makedirs(sourceFolder);

for f in originalFiles:
    shutil.copy(f, sourceFolder);

sp.call('java -cp target/sonarqube-repair-0.1-SNAPSHOT-jar-with-dependencies.jar Main 2272', shell = True, cwd = 'sonarqube-repair')

path = 'sonarqube-repair/spooned/se'
spoonedFiles = [];
for r, d, f in os.walk(path):
    for file in f:
        if '.java' in file:
            spoonedFiles.append(os.path.join(r, file))

for f in spoonedFiles:
    print(f)

for o in originalFiles:
    for s in spoonedFiles:
        if(o.split('/')[-1] == s.split('/')[-1]):
            if(not filecmp.cmp(o, s)):
                shutil.copy(s, o);
            break;

sp.call('git commit -a -m "Next should call hasNext and throw a NoSuchElementException"', shell = True, cwd = project);
sp.call('hub fork --remote-name=origin', shell = True, cwd = project);
sp.call('git push origin IteratorNextException', shell = True, cwd = project);
