#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject


class PipelineData(BaseObject):

    def __init__(self, input):
        # Original Input
        self.Input = input

        # Input Language | List of EmeraldAI.Entities.BaseObject.Word objects | List of parameters
        self.Language = None
        self.WordList = None
        self.ParameterList = None

        # Input with parameterized data
        self.ParameterizedInput = None

        # Current Context | Current User
        self.Context = None
        self.User = None

        # Response | Response found
        self.Answer = None
        self.AnswerFound = False

        # Pattern | Pattern Found
        self.Pattern = None
        self.PatternFound = False

        # List of Errors
        self.Error = None
