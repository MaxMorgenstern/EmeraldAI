#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import os
import traceback
import string
import random
import time

def GetDirHash(directory):
    SHAhash = hashlib.sha1()
    if not os.path.exists (directory):
        return -1

    try:
        for root, _, files in os.walk(directory):
            for names in files:
                filepath = os.path.join(root,names)
                try:
                    f1 = open(filepath, 'rb')
                except:
                    f1.close()
                    continue

                while 1:
                    buf = f1.read(4096)
                    if not buf : break
                    SHAhash.update(hashlib.sha1(buf).hexdigest())

                f1.close()
    except:
        traceback.print_exc()
        return -2

    return SHAhash.hexdigest()


def GenHash(seed=None, length=5, useDigits=False):
    if(seed is None):
        seed = time.time()
    base = string.ascii_letters+string.digits if useDigits else string.ascii_letters
    random.seed(seed)
    hash_value = ""
    for _ in range(length):
        hash_value += random.choice(base)
    return hash_value
