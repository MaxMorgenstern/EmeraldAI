#!/usr/bin/python

class CleanMdashesExtension():
    def cleanup(self, text):
        return text.replace('o', 'a')
