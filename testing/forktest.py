#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

print "go"

import multiprocessing
from multiprocessing import Queue
from multiprocessing import Manager
import sys


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
    time.sleep(1)
    return_dict[procnum] = procval


if __name__ == '__main__':
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
