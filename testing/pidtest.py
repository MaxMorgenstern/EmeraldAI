#/usr/bin/env python

import os
import sys

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
