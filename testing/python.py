#!/usr/bin/python
# coding=utf-8
#
#
#import imp
#imp.load_module("mydummyname")

import mydummyname
from mydummyname.CleanMdashesExtension import CleanMdashesExtension

import re   # Regex
import os   # I/O

print mydummyname.cleanup("Hello, World!")

print CleanMdashesExtension().cleanup("Hello, World")

print "--------------"

class SimpleNLP(object):
  def DetectLanguage(self, input):
    #TODO - split word_DE and word_EN out in file

    # 207 most common words in germen + hallo = 208
    #words_DE = ["die", "der", "und", "in", "zu", "den", "das", "nicht", "von", "sie", "ist", "des", "sich", "mit", "dem", "dass", "er", "es", "ein", "ich", "auf", "so", "eine", "auch", "als", "an", "nach", "wie", "im", "für", "man", "aber", "aus", "durch", "wenn", "nur", "war", "noch", "werden", "bei", "hat", "wir", "was", "wird", "sein", "einen", "welche", "sind", "oder", "zur", "um", "haben", "einer", "mir", "über", "ihm", "diese", "einem", "ihr", "uns", "da", "zum", "kann", "doch", "vor", "dieser", "mich", "ihn", "du", "hatte", "seine", "mehr", "am", "denn", "nun", "unter", "sehr", "selbst", "schon", "hier", "bis", "habe", "ihre", "dann", "ihnen", "seiner", "alle", "wieder", "meine", "Zeit", "gegen", "vom", "ganz", "einzelnen", "wo", "muss", "ohne", "eines", "können", "sei", "ja", "wurde", "jetzt", "immer", "seinen", "wohl", "dieses", "ihren", "würde", "diesen", "sondern", "weil", "welcher", "nichts", "diesem", "alles", "waren", "will", "Herr", "viel", "mein", "also", "soll", "worden", "lassen", "dies", "machen", "ihrer", "weiter", "Leben", "recht", "etwas", "keine", "seinem", "ob", "dir", "allen", "großen", "Jahre", "Weise", "müssen", "welches", "wäre", "erst", "einmal", "Mann", "hätte", "zwei", "dich", "allein", "Herren", "während", "guten", "anders", "Liebe", "kein", "damit", "gar", "Hand", "Herrn", "euch", "sollte", "konnte", "ersten", "deren", "zwischen", "wollen", "denen", "dessen", "sagen", "bin", "Menschen", "gut", "darauf", "wurden", "weiß", "gewesen", "Seite", "bald", "weit", "große", "solche", "hatten", "eben", "andern", "beiden", "macht", "sehen", "ganze", "anderen", "lange", "wer", "ihrem", "zwar", "gemacht", "dort", "kommen", "Welt", "heute", "Frau", "werde", "derselben", "ganzen", "deutschen", "lässt", "vielleicht", "meiner", "hallo"]
    words_DE = self.ReadFile("data/", "commonwords_DE.txt")

    # 207 most common words in english + hello = 208
    #words_EN = ["the", "of", "and", "a", "to", "in", "is", "be", "that", "was", "he", "for", "it", "with", "as", "his", "I", "on", "have", "at", "by", "not", "they", "this", "had", "are", "but", "from", "or", "she", "an", "which", "you", "one", "we", "all", "were", "her", "would", "there", "their", "will", "when", "who", "him", "been", "has", "more", "if", "no", "out", "do", "so", "can", "what", "up", "said", "about", "other", "into", "than", "its", "time", "only", "could", "new", "them", "man", "some", "these", "then", "two", "first", "May", "any", "like", "now", "my", "such", "make", "over", "our", "even", "most", "me", "state", "after", "also", "made", "many", "did", "must", "before", "back", "see", "through", "way", "where", "get", "much", "go", "well", "your", "know", "should", "down", "work", "year", "because", "come", "people", "just", "say", "each", "those", "take", "day", "good", "how", "long", "Mr", "own", "too", "little", "use", "US", "very", "great", "still", "men", "here", "life", "both", "between", "old", "under", "last", "never", "place", "same", "another", "think", "house", "while", "high", "right", "might", "came", "off", "find", "states", "since", "used", "give", "against", "three", "himself", "look", "few", "general", "hand", "school", "part", "small", "American", "home", "during", "number", "again", "Mrs", "around", "thought", "went", "without", "however", "govern", "dont", "does", "got", "public", "United", "point", "end", "become", "head", "once", "course", "fact", "upon", "need", "system", "set", "every", "war", "put", "form", "water", "took", "program", "present", "government", "thing", "told", "possible", "group", "large", "until", "hello"]
    words_EN = self.ReadFile("data/", "commonwords_EN.txt")


    exactMatch_DE = re.compile(r'\b%s\b' % '\\b|\\b'.join(words_DE), flags=re.IGNORECASE)
    count_DE = len(exactMatch_DE.findall(input))

    exactMatch_EN = re.compile(r'\b%s\b' % '\\b|\\b'.join(words_EN), flags=re.IGNORECASE)
    count_EN = len(exactMatch_EN.findall(input))

    if(count_EN > count_DE):
      return "en"

    return "de"

  def WordSegmentation(self, input):
    segmentationRegex = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", flags=re.IGNORECASE)
    return segmentationRegex.findall(input)

  def RemoveStopwords(self, wordlist, language):
    stopwords = self.ReadFile("data/", "stopwords_{0}.txt".format(language.upper()))
    return [x for x in wordlist if x not in stopwords]

  def ReadFile(self, foldername, filename):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

    return [line.rstrip('\n').rstrip('\r') for line in open(os.path.join(script_dir, foldername, filename))]



detect_DE = SimpleNLP().DetectLanguage("Hallo, dies ist ein Test!")
print detect_DE
detect_EN = SimpleNLP().DetectLanguage("Hello my old friend!")
print detect_EN

list_DE = SimpleNLP().WordSegmentation("Hallo, dies ist ein Test!")
print list_DE
list_EN = SimpleNLP().WordSegmentation("Hello my old friend!")
print list_EN

list_clean_DE = SimpleNLP().RemoveStopwords(list_DE, detect_DE)
print list_clean_DE

list_clean_EN = SimpleNLP().RemoveStopwords(list_EN, detect_EN)
print list_clean_EN

print "--------------"









# Language Detection
# Sentence + Word Segmentation
# Word Tagging + Synonym detection
# Phrase Detection

# strip stoppwords

# Pattern Detection
# Context Pipeline
# Answer Pipeline
  # Answer selection
  # ELIZA fallback
# Customize Answer
# Train Conversation




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
