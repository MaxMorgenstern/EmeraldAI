#!/usr/bin/python
# -*- coding: utf-8 -*-

#import imp
#imp.load_module("mydummyname")

import mydummyname
from mydummyname.CleanMdashesExtension import CleanMdashesExtension

import re   # Regex
import os   # I/O

print os.path.dirname(__file__)
print os.path.basename(__file__)
print os.path.dirname(os.path.abspath(__file__))

class Global(object):
    Path = os.path.dirname(os.path.abspath(__file__)).rstrip("/") + "/"


print mydummyname.cleanup("Hello, World!")

print CleanMdashesExtension().cleanup("Hello, World")

print "--------------"

class SimpleNLP(object):
  def DetectLanguage(self, input):
    #TODO - split word_DE and word_EN out in file

    # 207 most common words in germen + hallo = 208
    words_DE = self.ReadFile("data/", "commonwords_DE.txt")

    # 207 most common words in english + hello = 208
    words_EN = self.ReadFile("data/", "commonwords_EN.txt")


    exactMatch_DE = re.compile(r'\b%s\b' % '\\b|\\b'.join(words_DE), flags=re.IGNORECASE)
    count_DE = len(exactMatch_DE.findall(input))

    exactMatch_EN = re.compile(r'\b%s\b' % '\\b|\\b'.join(words_EN), flags=re.IGNORECASE)
    count_EN = len(exactMatch_EN.findall(input))

    if(count_EN > count_DE):
      return "en"

    return "de"

  def WordSegmentation(self, input):
    segmentationRegex = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\wÄÖÜäöüß\-]+", flags=re.IGNORECASE)
    return segmentationRegex.findall(input)

  def RemoveStopwords(self, wordlist, language):
    stopwords = self.ReadFile("data/", "stopwords_{0}.txt".format(language.upper()))
    return [x for x in wordlist if x not in stopwords]

  def ReadFile(self, foldername, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__)) #<-- absolute dir the script is in

    return [line.rstrip('\n').rstrip('\r') for line in open(os.path.join(script_dir, foldername, filename))]


print "Hallo, dies ist ein nötiger Test!"

detect_DE = SimpleNLP().DetectLanguage("Hallo, dies ist ein nötiger Test!")
print detect_DE
detect_EN = SimpleNLP().DetectLanguage("Hello my old friend!")
print detect_EN

list_DE = SimpleNLP().WordSegmentation("Hallo, dies ist ein nötiger Test!")
print list_DE
list_EN = SimpleNLP().WordSegmentation("Hello my old friend!")
print list_EN

list_clean_DE = SimpleNLP().RemoveStopwords(list_DE, detect_DE)
print list_clean_DE

list_clean_EN = SimpleNLP().RemoveStopwords(list_EN, detect_EN)
print list_clean_EN

print "--------------"
print "--------------"





import sqlite3 as lite
import sys

con = None

try:
    script_dir = Global.Path

    con = lite.connect(script_dir + 'data/' + 'thesaurus_DE.sqlite')
    con.text_factory = str

    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    print "SQLite version: %s" % data

    #cur.execute('SELECT * FROM synset WHERE synset.id = 1')
    cur.execute('SELECT * FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word = "Bank"')

    rows = cur.fetchall()

    for row in rows:
        print row


except lite.Error, e:

    print "Error %s:" % e.args[0]
    #sys.exit(1)

finally:
    print "Close DB Connection"
    if con:
        con.close()

#sys.exit(0)

print "--------------"

import json


class BaseObject(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


class PipelineData(BaseObject):
    def __init__(self, input):
      self.Input = input

      self.Language = None
      self.WordList = None
      self.WordlistClean = None
      self.SynonymList = None

      self.Context = None
      self.User = None

      self.Answer = None
      self.AnswerFound = False

      self.Pattern = None
      self.PatternFound = False

      self.Error = None

class Word(BaseObject):
  def __init__(self, input):
    self.Word = input
    self.Ranking = None
    self.IsStopWord = False

    self.SynonymList = None


ip = PipelineData("Test")
print ip.toJSON()



print "--------------"


cnx = None
try:
  import mysql.connector

  cnx = mysql.connector.connect(user='root', password='',
                                host='127.0.0.1',
                                database='thesaurus')
  #except mysql.connector.Error as err:
  #  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
  #    print("Something is wrong with your user name or password")
  #  elif err.errno == errorcode.ER_BAD_DB_ERROR:
  #    print("Database does not exist")
  #  else:
  #    print(err)

  cursor = cnx.cursor()

  cursor.execute('SELECT * FROM term, synset, term term2 WHERE synset.is_visible = 1 AND synset.id = term.synset_id AND term.synset_id AND term2.synset_id = synset.id AND term2.word = "Bank"')

  for row in cursor:
      print row

except:
  print "Mysql error"

finally:
  if(cnx):
    cnx.close()




import ConfigParser
config = ConfigParser.ConfigParser()
config.read(Global.Path + "base.conf")


print config.sections()
print config.get("Server", "Username")
print config.get("Server", "Password")

print config.getint("Server", "Testvalue")
print config.getboolean("Server", "Debug")

# .get(section, option)
# .getint(section, option)
# .getfloat(section, option)
# .getboolean(section, option)



class Animal():
    ant = 1
    bee = 2
    cat = 3
    dog = 4


print Animal.ant
print Animal.dog == Animal.cat



print "--------------"


"""
import logging
logging.basicConfig(filename='example.log',format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG ) # DEBUG INFO WARNING ERROR
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
"""

import logging
import logging.config

logging.config.fileConfig(Global.Path + "logging.conf")

logger = logging.getLogger('ExampleLogger')

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')



print "--------------"


print os.path.abspath(os.path.join('..'))
print os.path.abspath(os.path.join('..', 'EmeraldAI'))

sys.path.append(os.path.abspath(os.path.join('..')))
from EmeraldAI.Entities.Word import *

x = Word("hi")

print x.toJSON()



# Input Processing
  # Language Detection
  # Sentence + Word Segmentation
  # Word Tagging + Synonym detection
  # strip stoppwords

# Input Analyzer
  # Phrase Detection
  # Pattern Detection
  # Context Pipeline

# Response Processing
  # Answer Pipeline
    # Answer selection
    # ELIZA fallback
  # Customize Answer
  # Train Conversation


rules = {
    r"(.*)hey (.*)": [
        "Hey! I'm Ellie.",
        ],
    r"(.*)hi (.*)": [
        "Hi! I'm Ellie.",
        ],
    r"(.*)hello (.*)": [
        "Hello there. I'm Ellie.",
        ],
    r"(.*)drink (.*)": [
        "Bottoms up!",
        "Cheers!",
        ]
    }

default_responses = [
    "Very interesting",
    "I am not sure I understand you fully",
    "What does that suggest to you?",
    "Please continue",
    "Go on",
    "Do you feel strongly about that?",
    "Tell me more?",
    "Yes .. and?",
    "mmmm.",
    "And then what?",
    "Mmkay.",
    "What makes you say that?",
    "Aaaaah.",
    "Sure.",
    ]


import random

def respond(data):

    for pattern, responses in rules.items():
        compiledRegex = re.compile(pattern, flags=re.IGNORECASE)
        match = compiledRegex.match(data)
        if match:
          return random.choice(responses)
    return random.choice(default_responses)


 # https://github.com/christinac/ellie-slack/blob/master/plugins/ellie/ellie.py
 # https://www.smallsurething.com/implementing-the-famous-eliza-chatbot-in-python/

 # https://github.com/christinac/ellie-slack/blob/master/plugins/ellie/eliza.py

print respond("Hey There!")
print respond("I like to drink regulary")
print respond("This is the end of the world")


print "--------------"


# todo: add package check

import imp
try:
    imp.find_module('aiml')
    found = True
except ImportError:
    found = False


if(found):
    import aiml

    sessionId = 12345


    # Create the kernel and learn AIML files
    kernel = aiml.Kernel()

    if os.path.isfile("German-standalone.brn"):
        kernel.bootstrap(brainFile = "German-standalone.brn")
    else:
        kernel.bootstrap(learnFiles = "German-standalone.aiml", commands = "load aiml b")
        kernel.saveBrain("German-standalone.brn")

    kernel.setPredicate("name", "Brandy", sessionId)

    kernel.setBotPredicate("name", "Hugo")

    run = True
    while run:
        message = raw_input("Enter your message to the bot: ")
        if message == "quit" or message == "exit":
            run = False
        elif message == "save":
            kernel.saveBrain("German-standalone.brn")
        else:
            bot_response = kernel.respond(message, sessionId)
            # Do something with bot_response
            print bot_response


print "--------------"
print "--------------"
print "--------------"

import pip

def install(package):
    pip.main(['install', package])

print __name__
# Example
if __name__ == '__main__':
    install('aiml')


"""
class MyClass(object):

    staticvar = 999

    def __init__(self, name):
      self.name = name

    def hi(self):
        return 'Hello ' + self.name

    @staticmethod
    def example():
        return 'Static call'

    @classmethod
    def is_static_999(cls):
        return cls.staticvar == 999


xx = MyClass("Mama")
print xx.hi()

print xx.example()
print MyClass.example()

print xx.staticvar
print MyClass.staticvar

print xx.is_static_999()
print MyClass.is_static_999()

print "--------------"

class MyChildClass(MyClass):

    def __init__(self, name):
      self.name = name
      self.staticvar = 998


xx = MyChildClass("Papa")
print xx.hi()

print xx.example()
print MyChildClass.example()

print xx.staticvar
print MyChildClass.staticvar

print xx.is_static_999()
print MyChildClass.is_static_999()

"""
# https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/


"""
class MyClass:
    i = 12345

    @classmethod
    def hi(self):
        return 'hello world'

class WordProcessor(object):
    PLUGINS = []
    def process(self, text):
        for plugin in self.PLUGINS:
            text = plugin().cleanup(text)
        return text

    @classmethod
    def plugin(cls, plugin):
        cls.PLUGINS.append(plugin)

@WordProcessor.plugin
class LocalCleanMdashesExtension(object):
    def cleanup(self, text):
        return text.replace('o', 'a')

@WordProcessor.plugin
class LocalStripWhitespaceExtension(object):
    def cleanup(self, text):
        return text.replace(' ', '')


print "Hello, World!"

wp = WordProcessor()
print wp.process("Hello, World!")

"""


"""
counter = 100          # An integer assignment
miles   = 1000.0       # A floating point
name    = "John"       # A string

print counter
print miles
print name

count = 0
while (count < 9):
   print 'The count is:', count
   count = count + 1

print "Good bye!"


list3 = ["a", "b", "c", "d"]
list3.append("e")
print list3




def printme( str ):
   "This prints a passed string into this function"
   print str
   return

printme("This is a test")


x = MyClass()
print x.hi()

"""
