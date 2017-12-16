#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import itertools

class SerialFinder():
    _command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""
    _replace = "/sys/class/tty"
    _replaceWith = "/dev"


    def Find(self):
        proc = subprocess.Popen([self._command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        if len(out) < 2:
            return []

        return self.__split(out)

    def __groupSeparator(self, line):
        return line=='\n'

    def __split(self, data):
        lines = []
        for key, group in itertools.groupby(data, self.__groupSeparator):
            line = ''.join(str(e) for e in group)
            line = line.strip()
            if (len(line) > 1):
                lines.append(line.replace(self._replace, self._replaceWith))
        return lines
