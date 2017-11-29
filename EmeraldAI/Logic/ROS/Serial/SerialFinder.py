#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import itertools

class SerialFinder():
    _command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""

    def Find(self):

        proc = subprocess.Popen([self._command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        if len(out) < 2:
            return None

        return self.__split(out)

    def __groupSeparator(line):
        return line=='\n'

    def __split(data):
        lines = []
        for key, group in itertools.groupby(data, __groupSeparator):
            line = ''.join(str(e) for e in group)
            line = line.strip()
            if (len(line) > 1):
                lines.append(line.replace(replace, replaceWith))
        return lines
