#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import tarfile
url = "https://api.github.com/repos/MaxMorgenstern/EmeraldAI/releases"
response = urllib2.urlopen(url)
data = json.loads(response.read())

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

# TODO get current version
try:
	file = open("versionfile.txt", "r")
	v = file.read()
except Exception as e:
	v = "0.0.0"

print "Current version", v

highestVestion = v
highestVersionObject = None
for d in data:
	currentVersion = CleanTerm(d['tag_name'])
	if(IsVersionHigher(highestVestion, currentVersion)):
		highestVestion = currentVersion
		highestVersionObject = d

if (highestVersionObject == None):
	print "Already up to date"
	exit()

print "New highest version", highestVestion

file = open("versionfile.txt","w")
file.write(highestVestion)
file.close()


response = urllib2.urlopen(highestVersionObject['tarball_url'])
data = response.read()

filename = "currentVersion.tar.gz"
file_ = open(filename, 'w')
file_.write(data)
file_.close()

print "File downloaded"


tar = tarfile.open(filename, "r:gz")
tar.extractall("tmp_extract")
tar.close()

print "File extracted"

# TODO: move into destination

# TODO: update current version for next run

# TODO: delete everything left over in tmp folder



