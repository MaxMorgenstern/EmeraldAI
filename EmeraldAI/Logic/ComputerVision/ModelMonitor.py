#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.Modules import Hashing
from EmeraldAI.Logic.ComputerVision.ComputerVision import ComputerVision
from EmeraldAI.Logic.Logger import *

class ModelMonitor(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__HashFileName = "{0}.npy"
        self.__DatasetBasePath = os.path.join(Global.EmeraldPath, "Data", "ComputerVisionData")

    def CompareHash(self, datasetName, hashValue):
        path = os.path.join(self.__DatasetBasePath, datasetName)
        folderHash = Hashing.GetDirHash(path)
        return (folderHash == hashValue)

    def GetStoredHash(self, datasetName):
        try:
            storedHash = np.load(os.path.join(self.__DatasetBasePath, self.__HashFileName.format(datasetName))).item()
        except Exception:
            storedHash = 0
        return storedHash

    def Rebuild(self, datasetName, imageSize=None):
        try:
            storedHash = np.load(os.path.join(self.__DatasetBasePath, self.__HashFileName.format(datasetName))).item()
        except Exception:
            storedHash = 0

        if (self.CompareHash(datasetName, storedHash)):
            return

        FileLogger().Info("ModelMonitor: Rebuild {0} Model".format(datasetName))
        ComputerVision().TrainModel(datasetName, imageSize)
        path = os.path.join(self.__DatasetBasePath, datasetName)
        folderHash = Hashing.GetDirHash(path)
        np.save(os.path.join(self.__DatasetBasePath, self.__HashFileName.format(datasetName)), folderHash)
