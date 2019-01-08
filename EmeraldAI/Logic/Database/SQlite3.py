#!/usr/bin/python
# -*- coding: utf-8 -*-
from cachetools import cached
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *

class SQlite3(object):
    __metaclass__ = Singleton

    __Database = None

    def __init__(self):
        self.__Database = self.GetDB(Config().Get("Database", "SQliteDatabase"))

    def GetDB(self, database):
        return Worker(os.path.join(Global.EmeraldPath, "Data", "SqliteDB", database.rstrip(".sqlite") + ".sqlite"))

    @cached(cache={})
    def Execute(self, sql, args=None):
        return self.ExecuteDB(self.__Database, sql, args)

    def ExecuteDB(self, db, sql, args=None):
        db.execute(sql, args)
        return db.getLastrowid()

    @cached(cache={})
    def Fetchall(self, sql, args=None):
        return self.FetchallDB(self.__Database, sql, args)

    def FetchallCacheBreaker(self, sql, args=None):
        return self.FetchallDB(self.__Database, sql, args)

    def FetchallDB(self, db, sql, args=None):
        return db.execute(sql, args)

    def Disconnect(self):
        self.DisconnectDB(self.__Database)

    def DisconnectDB(self, db):
        db.close()


###############################################################################

# Copyright (c) 2014 Palantir Technologies
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#__author__ = "Shawn Lee"
#__email__ = "dashawn@gmail.com"
#__license__ = "MIT"
#
# Thread safe sqlite3 interface.

import sqlite3
import threading
import uuid

try:
    import queue as Queue  # module re-named in Python 3
except ImportError:
    import Queue


class Worker(threading.Thread):
    def __init__(self, file_name, max_queue_size=100):
        threading.Thread.__init__(self, name=__name__)
        self.daemon = True
        self._sqlite3_conn = sqlite3.connect(
            file_name, check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES)
        self._sqlite3_conn.text_factory = str
        self._sqlite3_cursor = self._sqlite3_conn.cursor()
        self._sql_queue = Queue.Queue(maxsize=max_queue_size)
        self._results = {}
        self._max_queue_size = max_queue_size
        self._select_events = {}
        self._close_event = threading.Event()
        self._close_lock = threading.Lock()
        self.start()

    def run(self):
        execute_count = 0
        for token, query, values in iter(self._sql_queue.get, None):
            if query:
                self._run_query(token, query, values)
                execute_count += 1
                if (self._sql_queue.empty() or
                        execute_count == self._max_queue_size):
                    self._sqlite3_conn.commit()
                    execute_count = 0

            if self._close_event.is_set() and self._sql_queue.empty():
                self._sqlite3_conn.commit()
                self._sqlite3_conn.close()
                return

    def _run_query(self, token, query, values):
        if query.lower().strip().startswith("select"):
            try:
                self._sqlite3_cursor.execute(query, values)
                self._results[token] = self._sqlite3_cursor.fetchall()
            except sqlite3.Error as err:
                self._results[token] = (
                    "Query returned error: %s: %s: %s" % (query, values, err))
            finally:
                self._select_events.setdefault(token, threading.Event())
                self._select_events[token].set()
        else:
            try:
                self._sqlite3_cursor.execute(query, values)
            except sqlite3.Error as err:
                # TODO
                print err

    def close(self):
        with self._close_lock:
            if not self.is_alive():
                return "Already Closed"
            self._close_event.set()
            self._sql_queue.put(("", "", ""), timeout=5)
            self.join()

    @property
    def queue_size(self):
        return self._sql_queue.qsize()

    def _query_results(self, token):
        try:
            self._select_events.setdefault(token, threading.Event())
            self._select_events[token].wait()
            return self._results[token]
        finally:
            self._select_events[token].clear()
            del self._results[token]
            del self._select_events[token]

    def execute(self, query, values=None):
        if self._close_event.is_set():
            return "Close Called"
        values = values or []
        token = str(uuid.uuid4())
        self._sql_queue.put((token, query, values), timeout=5)

        if query.lower().strip().startswith("select"):
            return self._query_results(token)

    def getLastrowid(self):
        return self._sqlite3_cursor.lastrowid
