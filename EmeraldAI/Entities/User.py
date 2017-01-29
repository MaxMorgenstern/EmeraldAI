#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from datetime import datetime

# TODO

class User(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    __cvTag = None

    Name = "Unknown"
    LastName = None
    FirstName = None

    Gender = "Male"
    Birthday = None

    LastSeen = None
    LastSpokenTo = None

    Properties = []

    Formal = True
    Trainer = False
    Admin = False

    Updated = None

    def SetUserByCVTag(self, cvTag):
        self.__cvTag = cvTag
        # TODO - get details from DB

        self.Updated = datetime.now().strftime("%H%M")

