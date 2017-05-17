#/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import Pid


if(Pid.HasPid("pidtest")):
	sys.exit()
Pid.Create("pidtest")
try:
    while True:
    	continue
finally:
	Pid.Remove("pidtest")


"""
pidfileFormat = "{0}.pid"


def Create(name):
	pid = str(os.getpid())
	file(pidfileFormat.format(name), 'w').write(pid)

def Remove(name):
	os.unlink(pidfileFormat.format(name))

def HasPid(name):
	if os.path.isfile(name):
	    print "%s already exists, exiting" % name
	    return True
	return False

print sys.argv[0]
print os.path.realpath(__file__)



if(HasPid("pidtest")):
	sys.exit()
Create("pidtest")
try:
    # Do some actual work here
    while True:
    	continue
finally:
	Remove("pidtest")
"""




"""
pid = str(os.getpid())
pidfile = "pidtest.pid"

if os.path.isfile(pidfile):
    print "%s already exists, exiting" % pidfile
    sys.exit()
file(pidfile, 'w').write(pid)
try:
    # Do some actual work here
    while True:
    	continue
finally:
    os.unlink(pidfile)
"""
