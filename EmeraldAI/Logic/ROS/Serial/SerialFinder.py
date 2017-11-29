#!/usr/bin/python
# -*- coding: utf-8 -*-

class SerialFinder():
    _command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""

    def Find(self):

        proc = subprocess.Popen([self._command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        if len(out) < 2:
            return None

        print out
