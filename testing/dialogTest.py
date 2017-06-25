#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

# Training #############
from EmeraldAI.Logic.Trainer.DialogTrainer import *

start_time = time.time()

dt = DialogTrainer()

language = "de"
#data=""
data = """Q / A;Requirement;Sentence;Has Category;Set Category;Action
Q;;Guten Abend;;Greeting;
Q;;Guten Morgen;;Greeting;
Q;;Guten Tag;;Greeting;
Q;;Moin Moin;;Greeting;
Q;;Hallo;;Greeting;
Q;;Tach;;Greeting;
Q;;Tag auch;;Greeting;
Q;;Hallöchen;;Greeting;
A;;Hallo {name}.;Greeting;;
A;;Guten Tag {name}.;Greeting;;
A;;Guten Tag {name}. Wie kann ich Ihnen heute behilflich sein?;Greeting;Question;
A;;Ich wünsche Ihnen einen schönen guten Tag!;Greeting;;
A;User:Unknown;Guten Tag. Wie ist Ihr Name?;Greeting;Question|Name;
A;Time:lt1100|User:Unknown;Guten Morgen. Wie ist Ihr Name?;Greeting;Question|Name;
A;Time:lt1100;Ich wünsche Ihnen ebenfalls einen guten Morgen {name}.;Greeting;;
A;Time:lt1100;Guten Morgen {name}.;Greeting;;
A;Time:lt1100;Guten Morgen {name}. Wie geht es Ihnen heute Früh?;Greeting;Wellbeing|Question;
A;Time:lt1100;Hallo {name}, wie geht es Ihnen heute?;Greeting;Wellbeing|Question;
A;Time:lt1100|Day:Monday;Guten Morgen {name}. Ich hoffe Sie hatten ein schönes Wochenende?;Greeting;Weekend|Question;
A;Time:lt1100|Day:Monday;Guten Morgen {name}. Ich hoffe Sie hatten ein erholsames Wochenende?;Greeting;Weekend|Question;
A;Time:gt1700;Guten Abend {name}. Ich hoffe Sie hatten einen schönen Tag.;Greeting;Wellbeing|Question;
A;Time:gt1700;Guten Abend {name}.;Greeting;;
;;;;;
Q;;Gute Nacht;;Bye;
A;;Gute Nacht!;Bye;;
A;Time:lt1700;Ist es nicht ein bisschen früß um Gute Nacht zu sagen?;Bye;Question|Time;
;;;;;
Q;;Ciao;;Bye;
Q;;Bye;;Bye;
Q;;Auf Wiedersehen;;Bye;
Q;;Tschüss;;Bye;
Q;;Tschau;;Bye;
A;;Einen schönen Tag noch.;Bye;;
A;;Ich wünsche Ihnen noch einen schonen Tag.;Bye;;
A;Day:Friday;Ich wünsche Ihnen ein schönes Wochenende.;Bye;;
;;;;;
Q;;Wie ist dein Name;;Question|Name;
Q;;Wie heißt du;;Question|Name;
Q;;Wie nennt man dich;;Question|Name;
Q;;Wie wirst du genannt;;Question|Name;
A;;Mein Name ist {botname};Question|Name;;
A;User:Unknown;Mein Name ist {botname}. Wie ist Ihr Name?;Question|Name;Question|Name;
;;;;;
Q;;Welche Sprachen sprichst du;;Question|Language;
Q;;Wekche Sprachen kannst du sprechen;;Question|Language;
A;;Ich verstehe folgende Sprachen: {botlanguages};Question|Language;;
;;;;;
Q;;*;;;
A;WordType:Curseword;Und Sie erwarten nun dass ich darauf reagiere?;;;EndConversation
A;WordType:Curseword;Haben Sie sonst noch etwas dass Sie los werden wollen?;;;EndConversation
;;;;;
Q;;Mein Name ist {firstname}{lastname};;Name;
Q;;Ich heiße {firstname}{lastname};;Name;
Q;;Nenn mich {firstname}{lastname};;Name;
Q;;Ich bin {firstname}{lastname};;Name;
Q;;{firstname};;Name;
Q;;{lastname};;Name;
Q;;{firstname}{lastname};;Name;
A;WordType:Firstname;Hallo {firstname};Name;;StoreName
A;WordType:Firstname|WordType:Lastname;Hallo {nametitle}{fullname};Name;;StoreName
A;WordType:Lastname;Hallo {nametitle}{lastname};Name;;StoreName
;;;;;
Q;;Wie geht es dir?;;Wellbeing|Question;
Q;;Wie ist dein aktueller Status?;;Wellbeing|Question;
A;;Meine Batterie ist bei {botbattery}.;Wellbeing|Question;;
A;UserType:Admin|BotStatus:eq1;Meine Batterie ist bei {botbattery}. Folgender Eintrag ist im Status Log: {botstatus};Wellbeing|Question;;
A;UserType:Admin|BotStatus:gt1;Meine Batterie ist bei {botbattery}. Folgende Einträge stind im Status Log: {botstatus};Wellbeing|Question;;
"""

data = """Q;;Wer ist {firstname}{lastname};;Question;
Q;;Wer war {firstname}{lastname};;Question;
Q;;Wer war {firstname}{lastname};;Question;
Q;;Was ist *;;Question;
Q;;Was war *;;Question;
A;;{result};Question;;Wikipedia
"""

data = """Q;;TRIGGER_FACEAPP_ON;;TRIGGER;
A;;Danke, dass Sie mein Display wieder eingeschatet haben.;TRIGGER;;
A;;Danke! Sehr nett von Ihnen.;TRIGGER;;
;;;;;
Q;;TRIGGER_FACEAPP_OFF;;TRIGGER;
A;User:Unknown;Hey, wer hat das List aus gemacht?;TRIGGER;;
A;;{name} warum haben Sie mein Display deaktiviert?;TRIGGER;;
A;;Das ist aber nicht nett {name}. Machen Sie bitte mein Display wieder an.;TRIGGER;;"""

#dt.TrainCSV(data, language)
print("--- %s seconds ---" % (time.time() - start_time))

# Resolving #############

from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse
from EmeraldAI.Entities.PipelineArgs import PipelineArgs


from EmeraldAI.Entities.NLPParameter import NLPParameter

def doWork(inputString):

    #print("processInput() done --- %s seconds ---" % (time.time() - start_time))
    #print inputString
    pa = PipelineArgs(inputString)

    # THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
    pa = ProcessInput().Process(pa)
    #print("processInput() done --- %s seconds ---" % (time.time() - start_time))

    dialogResult = AnalyzeScope().Process(pa)
    #print("AnalyzeScope() done --- %s seconds ---" % (time.time() - start_time))

    #print dialogResult.SentenceList
    #print ""

    #if dialogResult.SentenceList != None and len(dialogResult.SentenceList) > 0:
        #print random.choice(dialogResult.GetSentencesWithHighestValue())

    result = ProcessResponse().Process(dialogResult)
    print inputString, "  -  ", result.Response
    #print dialogResult.GetRandomSentenceWithHighestValue().GetSentenceString()

    #print("--- %s seconds ---" % (time.time() - start_time))


def doWorkDyn(inputString):

    #print("processInput() done --- %s seconds ---" % (time.time() - start_time))
    #print inputString
    pa = PipelineArgs(inputString)

    # THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
    pa = ProcessInput().ProcessAsync(pa)
    #print "Wordlist", pa.WordList
    #print "ParameterList", pa.ParameterList

    #print("processInput() done --- %s seconds ---" % (time.time() - start_time))

    dialogResult = AnalyzeScope().Process(pa)
    #print("AnalyzeScope() done --- %s seconds ---" % (time.time() - start_time))

    #print "Sentence List after Scope Analyze", dialogResult.SentenceList
    #print ""

    #if dialogResult.SentenceList != None and len(dialogResult.SentenceList) > 0:
        #print random.choice(dialogResult.GetSentencesWithHighestValue())

    #print dialogResult.toJSON()

    result = ProcessResponse().Process(dialogResult)
    print inputString, "  -  ", result.Response
    #print dialogResult.GetRandomSentenceWithHighestValue().GetSentenceString()

    #print("--- %s seconds ---" % (time.time() - start_time))

"""
from EmeraldAI.Logic.Modules import Global
words_DE = Global.ReadDataFile("Commonwords", "de.txt")
doWork(" ".join(words_DE))
"""

param = NLPParameter()

param.ParameterDictionary["Name"] = "Max"
param.ParameterDictionary["User"] = "Max"
param.ParameterDictionary["Input"] = "Hugo"
param.ParameterDictionary["Result"] = "ein kleiner Troll"

print "Start..."

doWorkDyn("Warmup")
print ""
print ""
print ""

#doWorkDyn("TRIGGER_FACEAPP_ON")


#start_time = time.time()
#doWork("Guten Abend Peter")
#doWork("Guten abend, Wer war Freddy Mercury")
#doWork("Wer war Freddy Mercury")
#doWork("Was ist 23 plus 12?")
#doWork("Hallöchen")
#doWork("Gute Nacht")
#print("END ROW: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
doWorkDyn("Guten Abend Otto")
#   doWorkDyn("Guten abend, Wer war Freddy Mercury")
doWorkDyn("Was ist drei plus sieben?")
doWorkDyn("Was ist dreiundzwanzig plus sieben?")
doWorkDyn("Was ist 23 plus 12?")
doWorkDyn("Wer ist Barack Obama")
doWorkDyn("Was ist Tschernobyl")
doWorkDyn("Bist du ein Mensch?")
doWorkDyn("Hilfe")
doWorkDyn("Gute Nacht")
print("END DYN: --- %s seconds ---" % (time.time() - start_time))

#start_time = time.time()
#doWorkDyn("Guten Abend Peter")
#doWorkDyn("Guten abend, Wer war Freddy Mercury")
#doWorkDyn("Was ist drei plus sieben?")
#doWorkDyn("Was ist 23 plus 12?")
#doWorkDyn("Hallöchen")
#doWork("Gute Nacht")
#print("END DYN: --- %s seconds ---" % (time.time() - start_time))

#start_time = time.time()
#doWork("Guten Abend Peter")
#doWork("Guten abend, Wer war Freddy Mercury")
#doWork("Was ist drei plus sieben?")
#doWork("Was ist 23 plus 12?")
#doWork("Hallöchen, wie geht es dir")
#doWork("Wer war Freddy Mercury")
#doWork("Gute Nacht")
#print("END ROW: --- %s seconds ---" % (time.time() - start_time))




