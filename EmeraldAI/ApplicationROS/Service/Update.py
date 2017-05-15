#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import json
import tarfile
import shutil
from os.path import dirname, abspath
# Path to run in deployment folder
sys.path.append(dirname(dirname(abspath(__file__))))
# Path to run in service folder
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import Global

def CleanTerm(term):
    term = term.replace('-alpha', '')
    term = term.replace('-beta', '')
    term = term.replace('-', '')
    term = term.replace('v', '')
    return term

def IsVersionHigher(old, current):
    oldVersion = old.split('.')
    currentVersion = current.split('.')
    if(int(currentVersion[0]) > int(oldVersion[0])):
        return True
    if(int(currentVersion[1]) > int(oldVersion[1])):
        return True
    if(int(currentVersion[2]) > int(oldVersion[2])):
        return True
    return False

def MoveDirectory(src_dir, dest_dir):
    fileList = os.listdir(src_dir)
    for i in fileList:
        src = os.path.join(src_dir, i)
        dest = os.path.join(dest_dir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                MoveDirectory(src, dest)
                continue
            else:
                os.remove(dest)
        shutil.move(src, dest_dir)

releaseUrl = 'https://api.github.com/repos/MaxMorgenstern/EmeraldAI/releases'
response = urllib2.urlopen(releaseUrl)
releaseObjects = json.loads(response.read())

deploymentPath = os.path.join(Global.RootPath, 'Deployment')
Global.EnsureDirectoryExists(deploymentPath)
versionFilePath = os.path.join(deploymentPath, 'versionfile.txt')

downloadFilename = os.path.join(deploymentPath, 'currentVersion.tar.gz')


try:
    file = open(versionFilePath, 'r')
    highestVestion = file.read()
except Exception as e:
    highestVestion = '0.0.0'

highestVersionObject = None
for d in releaseObjects:
    currentVersion = CleanTerm(d['tag_name'])
    if(IsVersionHigher(highestVestion, currentVersion)):
        highestVestion = currentVersion
        highestVersionObject = d

if (highestVersionObject == None):
    print 'Already up to date'
    exit()


# download file
response = urllib2.urlopen(highestVersionObject['tarball_url'])
data = response.read()

file = open(downloadFilename, 'w')
file.write(data)
file.close()


# extract
tar = tarfile.open(downloadFilename, 'r:gz')
tar.extractall(deploymentPath)
extractedFolderName = tar.getnames()[0]
tar.close()


# move into destination
MoveDirectory(os.path.join(deploymentPath, extractedFolderName, 'EmeraldAI'), Global.EmeraldPath)


# update version
file = open(versionFilePath,'w')
file.write(highestVestion)
file.close()


# delete everything left over in tmp folder
os.remove(downloadFilename)
shutil.rmtree(os.path.join(deploymentPath, extractedFolderName))
