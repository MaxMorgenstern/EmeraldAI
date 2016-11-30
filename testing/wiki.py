#!/usr/bin/python
# -*- coding: utf-8 -*-

import wikipedia
wikipedia.set_lang("de")

print wikipedia.summary("Rolling Stones")


#ny = wikipedia.page("New York")
#print ny


print wikipedia.summary("The Rolling Stones", sentences=1)
