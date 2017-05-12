#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import json
import tarfile

def CleanTerm(term):
    term = term.replace("-alpha", "")
    term = term.replace("-beta", "")
    term = term.replace("-", "")
    term = term.replace("v", "")
    return term

def IsVersionHigher(old, current):
	oldVersion = old.split(".")
	currentVersion = current.split(".")
	if(int(currentVersion[0]) > int(oldVersion[0])):
		return True
	if(int(currentVersion[1]) > int(oldVersion[1])):
		return True
	if(int(currentVersion[2]) > int(oldVersion[2])):
		return True
	return False

releaseUrl = "https://api.github.com/repos/MaxMorgenstern/EmeraldAI/releases"
response = urllib2.urlopen(releaseUrl)
releaseObjects = json.loads(response.read())

versionFilePath = "versionfile.txt"

# TODO - point file into better location
try:
	file = open(versionFilePath, "r")
	highestVestion = file.read()
except Exception as e:
	highestVestion = "0.0.0"

highestVersionObject = None
for d in releaseObjects:
	currentVersion = CleanTerm(d['tag_name'])
	if(IsVersionHigher(highestVestion, currentVersion)):
		highestVestion = currentVersion
		highestVersionObject = d

if (highestVersionObject == None):
	print "Already up to date"
	exit()


# download file
response = urllib2.urlopen(highestVersionObject['tarball_url'])
data = response.read()

filename = "currentVersion.tar.gz"
file_ = open(filename, 'w')
file_.write(data)
file_.close()

# extract
tar = tarfile.open(filename, "r:gz")
tar.extractall("tmp_extract")
tar.close()



# TODO: move into destination


# update version
file = open(versionFilePath,"w")
file.write(highestVestion)
file.close()

# TODO: delete everything left over in tmp folder


