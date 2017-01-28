#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton

# TODO

class User(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    Name = "Unknown"
    LastName = None
    FirstName = None

    cvTag = None

    Gender = "Male"
    Birthday = None

    LastSeen = None
    LastSpokenTo = None

    Properties = []

    Formal = True
    Trainer = False
    Admin = False

    def SetUserByCVTag(self, cvTag):
        self.cvTag = cvTag

