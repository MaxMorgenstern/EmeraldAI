#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import multiprocessing
from multiprocessing import Queue
from multiprocessing import Manager
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Singleton import Singleton
import json

#from thread import start_new_thread
from threading import Thread

class fooo(object):
    __metaclass__ = Singleton

    bar = None
    ID = 1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



def exampleFunction():
    y = fooo()
    y.ID += 1
    print "exampleFunction", y.toJSON()


x = fooo()
x.ID = 1
x.bar = "Max"
print x.toJSON()

"""
start_new_thread(exampleFunction,())
time.sleep(1)
start_new_thread(exampleFunction,())
start_new_thread(exampleFunction,())
"""
t1 = Thread(target=exampleFunction, args=())
t1.setDaemon(True)
t1.start()

time.sleep(1)

t2 = Thread(target=exampleFunction, args=())
t2.setDaemon(True)
t2.start()

t3 = Thread(target=exampleFunction, args=())
t3.setDaemon(True)
t3.start()

time.sleep(5)

print "---"

print x.toJSON()

print "ENDE"
t1.join()
t2.join()
t3.join()

exit()

"""
while len(threads) > 0:
    try:
        # Join all threads using a timeout so it doesn't block
        # Filter out threads which have been joined or are None
        threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
    except KeyboardInterrupt:
        print "Ctrl-c received! Sending kill to threads..."
        for t in threads:
            t.kill_received = True

"""








class foo(object):
    __metaclass__ = Singleton

    bar = None
    ID = 1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def daemon(q):
    p = multiprocessing.current_process()
    print 'Starting:', p.name, p.pid
    sys.stdout.flush()
    time.sleep(2)
    i = 0
    while i < 5:
        print "daemon loop"
        q.put(i)
        time.sleep(2)
        i += 1
    print 'Exiting :', p.name, p.pid
    sys.stdout.flush()


def non_daemon(q):
    p = multiprocessing.current_process()
    print 'Starting:', p.name, p.pid
    sys.stdout.flush()
    i = 0
    while i < 5:
        print "non_daemon loop", p.name, p.pid
        time.sleep(1)
        i += 1
    print 'Exiting :', p.name, p.pid
    sys.stdout.flush()


def worker(procnum, return_dict):
    procval = procnum * 10
    time.sleep(2)
    x = foo()
    print x.toJSON()
    time.sleep(3)
    x.ID += 1
    print x.toJSON()
    return_dict[procnum] = procval


if __name__ == '__main__':
    test = foo()
    test.ID = 1
    test.bar = "Max"

    print test.toJSON()

    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,return_dict))
        jobs.append(p)
        p.start()
        print i
    print "for done"

    for proc in jobs:
        proc.join()
    print return_dict.values()

    test.ID += 100

    print test.toJSON()

exit()








if __name__ == '__main__':
    queue = Queue()

    d = multiprocessing.Process(name='daemon', target=daemon, args=(queue,))
    d.daemon = True

    n = multiprocessing.Process(
        name='non-daemon', target=non_daemon, args=(queue,))
    n.daemon = False

    n2 = multiprocessing.Process(
        name='non-daemon-2', target=non_daemon, args=(queue,))
    n2.daemon = False

    n2.start()
    d.start()
    time.sleep(1)
    n.start()

    i = 0
    while i < 10:
        print "main loop -------------------", i
        print queue.qsize()
        print queue.full()
        print queue.empty()
        if(queue.qsize() > 0):
            print queue.get_nowait()
            print "#"

        time.sleep(1)
        i += 1

    print "main done - waiting for N"

    d.terminate()
    n.join()

    print "main done - bye"
