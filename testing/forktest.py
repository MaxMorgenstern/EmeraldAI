#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, time, signal

def timeConsumingFunction():
    print "timeConsumingFunction sleep now"
    time.sleep(2)
    print "timeConsumingFunction done"

pid = os.fork()

print pid

if pid > 0:
    child = pid
else:
    timeConsumingFunction()
    os._exit(0)

time.sleep(1)
print "parent kill child"
os.kill(child, signal.SIGKILL)

t = time.time()
os.waitpid(child, 0)
print time.time() - t
