#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import NLP

#from EmeraldAI.Logic.SpeechProcessing.Google import *
#from EmeraldAI.Logic.SpeechProcessing.Ivona import *
from EmeraldAI.Logic.AliceBot import *
from EmeraldAI.Logic.Thesaurus import *
from EmeraldAI.Logic.Modules.Database import SQlite3

#google = Google()
#ivona = Ivona()
#alice = AliceBot("DE")

thesaurus = Thesaurus()
litedb = SQlite3.GetDB("brain")

def addToList(str_to_add, list_of_strings, language):
	str_to_add = NLP.Normalize(str_to_add, language)
	if str_to_add not in list_of_strings:
		list_of_strings.append(str_to_add)
	return list_of_strings

def processInputData(data):
	language = NLP.DetectLanguage(data)
	#wordSegments = NLP.WordSegmentation(data)
	#cleanWordSegments = NLP.RemoveStopwords(wordSegments, language)

	wordSegments = NLP.WordSegmentation(NLP.Normalize(data, language))
	cleanWordSegments = NLP.RemoveStopwords(wordSegments, language)

	for word in wordSegments:
		#normalizedWord = NLP.Normalize(word, language)
		stopword = word not in cleanWordSegments
		#print word + " - " + normalizedWord + " - " + str(stopword)
		synonymList = []
		synonymList = addToList(word, synonymList, language)
		synonyms = thesaurus.GetSynonyms(word)
		for synonym in synonyms:
			if synonym[0]:
				synonymList = addToList(synonym[0], synonymList, language)
			else:
				synonymList = addToList(synonym[1], synonymList, language)

		print synonymList


		sql = "SELECT * FROM Dialog_Keyword, Dialog_Trigger WHERE Dialog_Keyword.Normalized_Keyword IN ({wordlist}) AND Dialog_Keyword.ID = Dialog_Trigger.Keyword_ID;"
		finalsql = sql.format(wordlist = ','.join(['?']*len(synonymList)))
		result = SQlite3.Fetchall(litedb, finalsql, synonymList)
		print result

		# add result to global array initial priority
		# if result already present increase priority
			# stopwords = half increase
			# Dialog_Trigger.Priority

	# get sentence with highest priority
	# replace placeholder

	return ""



"""
INSERT OR IGNORE INTO Dialog_Keyword (Keyword, Normalized_Keyword, Stopword) VALUES ('', '')
INSERT OR IGNORE INTO Dialog_Keyword_Sentence (Keyword_ID, Sentence_ID) VALUES ('', '')
INSERT OR IGNORE INTO Dialog_Sentence (Sentence, Normalized_Sentence, Category, Language) VALUES ('', '', '', '')
INSERT OR IGNORE INTO Dialog_Trigger (Keyword_ID, Sentence_ID, Priority) VALUES ('', '')



SELECT * FROM Dialog_Keyword, Dialog_Trigger WHERE Normalized_Keyword = '' AND Dialog_Keyword.ID = Dialog_Trigger.Keyword_ID

"""



# Get Input
# NLP
# Find Answer in DB
	# Not Found Fallback to Eliza
	# Found - Good
# Train DB



# Username
# User Data

# Timestamp
#

loop = True

while(loop):
  #inputData = google.Listen()
  inputData = raw_input("Enter Response: ")
  #print "We got: '{0}'".format(inputData)

  if(inputData.lower() == 'ende' or inputData.lower() == 'beenden'):
  	loop = False
  elif(len(inputData) == 0):
    print "No Data found"
  else:
    #response = alice.GetResponse(inputData)
    response = processInputData(inputData)
    print "We respond: '{0}'".format(response)
    #audioPath = ivona.Speak(response)
    #os.system("afplay '{0}'".format(audioPath))
