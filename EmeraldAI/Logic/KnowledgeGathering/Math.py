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
        # print pi
        # print e
        # common constants
        # pi
        # e - euler
        # ...

    def CleanTerm(self, term):
        #term = re.sub(r'"(\d+) (\d+)"', r'\1\2', term)
        result = self.__ReplacePattern.sub(lambda x: self.__replaceWordDictionary[x.group()], term)
        return result


    def Calculate(self, term):
        # replace words with math func
        # make sure no bad words are in there
        # make sure it's a equation

        cleanTerm = self.CleanTerm(term.lower())

        print cleanTerm

        try:

            return eval(cleanTerm, self.__namespace)
        except:
            return None


"""

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

print text2int("seven billion one hundred million thirty one thousand three hundred thirty seven")
#7100031337

"""



