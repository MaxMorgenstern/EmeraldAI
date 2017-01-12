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

        keys = r'|'.join(self.__replaceWordDictionary.keys())
        self.__FindPattern = re.compile(r'\b(' + keys + r')\b', flags=re.IGNORECASE)
        #self.__FindWords = re.compile(r'\b[a-zA-Z]+\b', flags=re.IGNORECASE)

        values= r''
        for v in list(set(self.__replaceWordDictionary.values())):
            values += re.escape(v) + "|"

        self.__FindWords = re.compile(values + r'\b(' + r'[0-9]+|' + keys + r')\b', flags=re.IGNORECASE)


    def CleanTerm(self, term):
        # replace whitespace and dots in between numbers
        term = re.sub("(\d+)[\s.]+(\d+)", r"\1\2", term)
        # replace comma with dot
        term = term.replace(",", ".")
        #replace words with mathematical symbols
        result = self.__FindPattern.sub(lambda x: self.__replaceWordDictionary[x.group()], term)
        return result


    def Calculate(self, term):
        cleanTerm = self.CleanTerm(term.lower())
        try:
            return eval(cleanTerm, self.__namespace)
        except:
            return None


    def IsEquation(self, term):
        #t = self.CleanTerm(term)

        z = self.__FindWords.sub(lambda x: "-{0}-".format(x.group()), term)
        print term, " -  ", z.strip()

        g = self.__FindWords.findall(term)
        print g



        if self.__FindPattern.search(term) is not None:
            #print self.__FindPattern.search(term)
            return True

        numberCount = 0
        wasPreviousNumber = False
        for char in term:
            if char.isdigit():
                if not wasPreviousNumber:
                    numberCount += 1
                    wasPreviousNumber = True
            else:
                wasPreviousNumber = False
        if numberCount >= 2:
            return True

        return False


"""
TODO: make sure term is equation
TODO: add more operations mentioned in the safe_list
TODO: improve is equation - maybe split in in mathematical for single words/terms
"""
