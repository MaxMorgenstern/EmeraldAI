#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config


class IFTTT(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__apiKey = Config().Get("IFTTT", "APIKey")


    def TriggerWebhook(self, event, value1=None, value2=None, value3=None):
        url = 'https://maker.ifttt.com/trigger/{e}/with/key/{k}/'.format(e=event, k=self.__apiKey)
        payload = {'value1': value1, 'value2': value2, 'value3': value3}
        return requests.post(url, data=payload)
