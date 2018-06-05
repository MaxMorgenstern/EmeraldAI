#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2


downloadFilename = 'download-web-content.txt'
configURL = 'https://gist.githubusercontent.com/MaxMorgenstern/2780c7cc0a66fec2bb5abe7e83ca6261/raw/08de6ce2470f4ca29441fbe2124a97319e71de48/TestPublic'
response = urllib2.urlopen(configURL)

data = response.read()
print data

file = open(downloadFilename, 'w')
file.write(data)
file.close()

