#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.SpeechProcessing.Watson import Watson
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import Config

def RunSTT():
    sttProvider = Config().Get("SpeechToText", "Provider")
    if(sttProvider.lower() == "watson"):
        provider = Watson()
        provider.Listen()


if __name__ == "__main__":
    if(Pid.HasPid("STTLive")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("STTLive")

    try:
        RunSTT()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("STTLive")
