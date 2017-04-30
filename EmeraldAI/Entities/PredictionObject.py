#!/usr/bin/python
# -*- coding: utf-8 -*-
import operator
from EmeraldAI.Config.Config import *

class PredictionObject(object):
    def __init__(self, name, model, dictionary, maxDistance):
        self.Name = name
        self.Model = model
        self.Dictionary = dictionary
        self.PredictionResult = {}

        self.MaxPredictionDistance = maxDistance
        self.__UnknownUserTag = Config().Get("ComputerVision", "UnknownUserTag")

    def __RemoveUnknown(self, resultDict):
        for k in resultDict.keys():
          if k == "Unknown":
            resultDict.pop(k)
        return resultDict

    def GetBestPredictionResult(self, id, ignoreUnknown=False):
        resultDict = self.PredictionResult[id]
        if(ignoreUnknown):
            resultDict = self.__RemoveUnknown(resultDict)

        sortedDict = sorted(resultDict.items(), key=operator.itemgetter(1), reverse=True)
        if (len(sortedDict) == 0):
            return ()
        return sortedDict[0]

    def AddPrediction(self, id, key, distance):
        if(self.PredictionResult.has_key(id)):
            if(self.PredictionResult[id].has_key(key)):
                self.PredictionResult[id][key] += (self.MaxPredictionDistance - distance)
            else:
                self.PredictionResult[id][key] = (self.MaxPredictionDistance - distance)
        else:
            self.PredictionResult[id] = {}
            self.PredictionResult[id][key] = (self.MaxPredictionDistance - distance)

    def ThresholdReached(self, threshold):
        if len(self.PredictionResult) > 0:
            for key, resultSet in self.PredictionResult.iteritems():
                maxKey = max(resultSet.iteritems(), key=operator.itemgetter(1))[0]
                if maxKey != self.__UnknownUserTag and threshold < resultSet[maxKey]:
                    return True
        return False

    def ResetResult(self):
        self.PredictionResult = {}

    def __repr__(self):
         return "Result:{0}".format(self.PredictionResult)

    def __str__(self):
         return "Result:{0}".format(self.PredictionResult)

