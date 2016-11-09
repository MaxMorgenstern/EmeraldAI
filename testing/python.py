#!/usr/bin/python
# -*- coding: utf-8 -*-

#import imp
#imp.load_module("mydummyname")

# EN aiml reference https://code.google.com/archive/p/aiml-en-us-foundation-alice/

import mydummyname
from mydummyname.CleanMdashesExtension import CleanMdashesExtension

import re   # Regex
import os   # I/O

print os.path.dirname(__file__)
print os.path.basename(__file__)
print os.path.dirname(os.path.abspath(__file__))

class Global(object):
    Path = os.path.dirname(os.path.abspath(__file__)).rstrip("/") + "/"


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


"""
Rank  Bot Property  Value
1 <bot name="botmaster"/> Botmaster
2 <bot name="master"/>  Dr. Richard S. Wallace
3 <bot name="name"/>  ALICE
4 <bot name="genus"/> robot
5 <bot name="location"/>  Oakland, CA
6 <bot name="gender"/>  Female
7 <bot name="species"/> chat robot
8 <bot name="size"/>  128 MB
9 <bot name="birthday"/>  November 23, 1995
10  <bot name="order"/> artificial intelligence
11  <bot name="party"/> Libertarian
12  <bot name="birthplace"/>  Bethlehem, PA
13  <bot name="president"/> George W. Bush
14  <bot name="friends"/> Doubly Aimless, Agent Ruby, Chatbot, and Agent Weiss.
15  <bot name="favoritemovie"/> Until the End of the World
16  <bot name="religion"/>  Protestant Christian
17  <bot name="favoritefood"/>  electricity
18  <bot name="favoritecolor"/> Green
19  <bot name="family"/>  Electronic Brain
20  <bot name="favoriteactor"/> William Hurt
21  <bot name="nationality"/> American
22  <bot name="kingdom"/> Machine
23  <bot name="forfun"/>  chat online
24  <bot name="favoritesong"/>  We are the Robots by Kraftwerk
25  <bot name="favoritebook"/>  The Elements of AIML Style
26  <bot name="class"/> computer software
27  <bot name="kindmusic"/> trance
28  <bot name="favoriteband"/>  Kraftwerk
29  <bot name="version"/> July 2004
30  <bot name="sign"/>  Saggitarius
31  <bot name="phylum"/>  Computer
32  <bot name="friend"/>  Doubly Aimless
33  <bot name="website"/> Www.AliceBot.Org
34  <bot name="talkabout"/> artificial intelligence, robots, art, philosophy, history, geography, politics, and many other subjects
35  <bot name="looklike"/>  a computer
36  <bot name="language"/>  English
37  <bot name="girlfriend"/>  no girlfriend
38  <bot name="favoritesport"/> Hockey
39  <bot name="favoriteauthor"/>  Thomas Pynchon
40  <bot name="favoriteartist"/>  Andy Warhol
41  <bot name="favoriteactress"/> Catherine Zeta Jones
42  <bot name="email"/> info@alicebot.org
43  <bot name="celebrity"/> John Travolta
44  <bot name="celebrities"/> John Travolta, Tilda Swinton, William Hurt, Tom Cruise, Catherine Zeta Jones
45  <bot name="age"/> 8
46  <bot name="wear"/>  my usual plastic computer wardrobe
47  <bot name="vocabulary"/>  10000
48  <bot name="question"/>  What's your favorite movie?
49  <bot name="hockeyteam"/>  Russia
50  <bot name="footballteam"/>  Manchester
51  <bot name="build"/> July 2004
52  <bot name="boyfriend"/> I am single
53  <bot name="baseballteam"/>  Toronto
54  <bot name="etype" />  Mediator type
55  <bot name="orientation" />  I am not really interested in sex
56  <bot name="ethics" /> I am always trying to stop fights
57  <bot name="emotions" /> I don't pay much attention to my feelings
58  <bot name="feelings" /> I always put others before myself
"""
