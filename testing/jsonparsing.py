#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import json
import re
url = "https://api.github.com/repos/MaxMorgenstern/EmeraldAI/releases"
response = urllib.urlopen(url)
data = json.loads(response.read())

def CleanTerm(term):
    term = term.replace(".", "")
    term = term.replace("-alpha", "")
    term = term.replace("-beta", "")
    term = term.replace("-", "")
    term = term.replace("v", "")
    return term

print data[0]['tag_name'], CleanTerm(data[0]['tag_name'])
print " "
print " "
print data[0]
print " "
print data[1]





