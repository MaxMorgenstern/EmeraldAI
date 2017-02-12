#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton

from EmeraldAI.Entities.Bot import Bot
from EmeraldAI.Entities.User import User

# TODO

class Context(BaseObject):
    __metaclass__ = Singleton

    def __init__(self)
        self.Category = "Greeting"    # Current Category

        self.Status = "inactive"    # current status if the robot is busy or not
        self.Action = None    # Current Action
        self.Task = None    # Current Task (could be part of the action)

        self.Queue = None   # Queue with (Tasks/Actions) to do next

        self.User = User()  # User reference
        self.Bot = Bot()    # Bot Reference

        self.Location = None
        self.Mode = "Live" # Live or Training ...

        self.History = None # list of historical...
