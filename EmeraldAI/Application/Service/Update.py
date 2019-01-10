#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import json
import tarfile
import shutil
from os.path import dirname, abspath
from distutils.version import StrictVersion
# Path to run in deployment folder
sys.path.append(dirname(dirname(abspath(__file__))))
# Path to run in service folder
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *

def CleanTerm(term):
    term = term.replace('-alpha', '')
    term = term.replace('-beta', '')
    term = term.replace('-', '')
    term = term.replace('v', '')
    return term

def IsVersionHigher(old, current):
    if old == 'beta':
        return True
    return (StrictVersion(current) > StrictVersion(old))

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

def GetFileList(dirPath):
    if (not dirPath.endswith("/")):
        dirPath += "/"
    fileList = []
    for root, dirs, files in os.walk(dirPath):
        # skip "." files and folder
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for filename in files:
            fileList.append(os.path.join(root, filename).replace(dirPath, '/'))

    return fileList

def Purge(basePath, fileList):
    for file in fileList:
        fullPath = os.path.normpath(os.path.join(basePath, "."+file))
        print "Delete:", fullPath
        os.remove(fullPath)


PIDName = "Update"
if(Pid.HasPid(PIDName)):
    print "Update already running"
    exit()
Pid.Create(PIDName)


try:

    deploymentPath = os.path.join(Global.RootPath, 'Deployment')
    Global.EnsureDirectoryExists(deploymentPath)
    versionFilePath = os.path.join(deploymentPath, 'versionfile.txt')

    downloadFilename = os.path.join(deploymentPath, 'currentVersion.tar.gz')

    if Config().GetBoolean("DEFAULT", "Beta"): # Default False
        highestVersionNumber = 'beta'

        betaUrl = 'https://api.github.com/repos/MaxMorgenstern/EmeraldAI/branches'
        response = urllib2.urlopen(betaUrl)
        releaseObjects = json.loads(response.read())

        betaBranch = None
        for d in releaseObjects:
            if d['name'] != 'master':
                betaBranch = d['name']

        if betaBranch is None:
            print "Can not find recent beta branch"
            exit()

        tarballUrl = 'https://github.com/MaxMorgenstern/EmeraldAI/tarball/{0}'.format(betaBranch)

        print "Found beta branch '{0}'".format(betaBranch)

        print "Download latest beta version"

        response = urllib2.urlopen(tarballUrl)
        data = response.read()


    else:

        releaseUrl = 'https://api.github.com/repos/MaxMorgenstern/EmeraldAI/releases'
        response = urllib2.urlopen(releaseUrl)
        releaseObjects = json.loads(response.read())

        try:
            file = open(versionFilePath, 'r')
            localVersion = file.read()
        except Exception as e:
            print 'Data about currently installed version missing'
            localVersion = '0.0.0'

        highestVersionObject = None
        highestVersionNumber = localVersion

        for d in releaseObjects:
            gitVersion = CleanTerm(d['tag_name'])
            if(IsVersionHigher(highestVersionNumber, gitVersion)):
                highestVersionNumber = gitVersion
                highestVersionObject = d

        if (highestVersionObject is None):
            print "Already up to date. Version: '{0}'".format(localVersion)
            exit()

        print "Local version '{0}' - Latest release {1}".format(localVersion, highestVersionNumber)

        print "Download latest release"

        response = urllib2.urlopen(highestVersionObject['tarball_url'])
        data = response.read()


    # download file
    file = open(downloadFilename, 'w')
    file.write(data)
    file.close()

    print "Extract files"

    # extract
    tar = tarfile.open(downloadFilename, 'r:gz')
    tar.extractall(deploymentPath)
    extractedFolderName = tar.getnames()[0]
    tar.close()

    print "Remove deprecated files"

    sourceFileList = GetFileList(os.path.join(deploymentPath, extractedFolderName, 'EmeraldAI'))
    targetFileList = GetFileList(Global.EmeraldPath)
    diffList =  list(set(targetFileList) - set(sourceFileList))
    diffList = [x for x in diffList if not x.endswith('.pyc')
        and not x.endswith('.mdl')
        and not x.endswith('.npy')
        and not x.endswith('.mp3')
        and not x.endswith('.config')
        and not x.endswith('.sqlite')
        and not x.endswith('.log')
        and not x.startswith('/Data/ComputerVisionData')]

    Purge(Global.EmeraldPath, diffList)

    print "Update files"

    # move into destination
    MoveDirectory(os.path.join(deploymentPath, extractedFolderName, 'EmeraldAI'), Global.EmeraldPath)

    # update version
    file = open(versionFilePath,'w')
    file.write(highestVersionNumber)
    file.close()


    # delete everything left over in tmp folder
    os.remove(downloadFilename)
    shutil.rmtree(os.path.join(deploymentPath, extractedFolderName))

finally:
    Pid.Remove(PIDName)
