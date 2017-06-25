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

        # TODO - config
        self.__equationThreshold = 2

        self.__safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                            'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']

        self.__replaceWordDictionary = OrderedDict()
        replaceWords = Global.ReadDataFile("Math", "de.txt")
        for word in replaceWords:
            if(len(word) > 1):
                wordArray = word.split("|")
                self.__replaceWordDictionary[wordArray[1]] = wordArray[0]

        keys = r'|'.join(self.__replaceWordDictionary.keys())
        self.__FindPattern = re.compile(r'\b(' + keys + r')\b', flags=re.IGNORECASE)

        values= ''
        for v in list(set(self.__replaceWordDictionary.values())):
            values += re.escape(v) + "|"
        self.__FindWords = re.compile(values + r'[0-9]+|\b(?:' + keys + r')\b', flags=re.IGNORECASE)


    def CleanTerm(self, term):
        # replace whitespace and dots in between numbers
        term = re.sub("(\d+)[\s.]+(\d+)", r"\1\2", term)
        # replace comma with dot
        term = term.replace(",", ".")

        # make sure we onky leave mathematical data
        result = self.__FindWords.findall(term)
        strippedTerm = " ".join(result)

        # again replace whitespace and dots in between numbers
        strippedTerm = re.sub("(\d+)[\s.]+(\d+)", r"\1\2", strippedTerm)

        #replace words with mathematical symbols
        result = self.__FindPattern.sub(lambda x: self.__replaceWordDictionary[x.group()], strippedTerm)
        return result


    def Calculate(self, term):
        cleanTerm = self.CleanTerm(term.lower())
        try:
            return eval(cleanTerm, self.__namespace)
        except:
            return None


    def IsEquation(self, sentence):
        results = self.__FindWords.findall(sentence)
        if(len(results) >= self.__equationThreshold):
            return True
        return False


    def IsMathematicalWord(self, word):
        if self.__FindWords.search(word) is not None:
            return True
        return False


"""
TODO: add more operations mentioned in the safe_list
TODO: Line 25 - not only german file! move to config
"""
