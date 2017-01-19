#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton

class User(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    # TODO

    ID = None
    Name = None
    LastName = None
    UsedName = None

    Gender = "Male"
    Birthday = None

    LastSeen = None
    LastSpokenTo = None

    Properties = []

    Formal = True
    Trainer = False
    Admin = False

    __init__(self, ID, Name, Formal=True, Trainer=False, Admin=False):
        self.ID = ID
        self.Name = Name

        self.Formal = Formal
        self.Trainer = Trainer
        self.Admin = Admin
        # TODO - load data from DB
