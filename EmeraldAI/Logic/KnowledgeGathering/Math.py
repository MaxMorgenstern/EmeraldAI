#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import math
import re
from collections import OrderedDict
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global


class Math(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__namespace = vars(math).copy()
        self.__namespace['__builtins__'] = None

        self.__safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                            'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']

        self.__replaceWordDictionary = OrderedDict()
        replaceWords = Global.ReadDataFile("Math", "de.txt")
        for word in replaceWords:
            if(len(word) > 1):
                wordArray = word.split("|")
                self.__replaceWordDictionary[wordArray[1]] = wordArray[0]

        self.__ReplacePattern = re.compile(r'\b(' + '|'.join(self.__replaceWordDictionary.keys()) + r')\b')


        # https://docs.python.org/2/library/math.html
        # pi = math.pi
        # e = math.e


    def CleanTerm(self, term):
        # replace whitespace and dots in between numbers
        term = re.sub("(\d+)[\s.]+(\d+)", r"\1\2", term)
        # replace comma with dot
        term = term.replace(",", ".")
        #replace words with mathematical symbols
        result = self.__ReplacePattern.sub(lambda x: self.__replaceWordDictionary[x.group()], term)
        return result


    def Calculate(self, term):
        # replace words with math func
        # make sure no bad words are in there
        # make sure it's a equation

        cleanTerm = self.CleanTerm(term.lower())


        try:
            return eval(cleanTerm, self.__namespace)
        except:
            return None





