#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

# TODO: Reset to factory settings and clear database


"""

DELETE FROM Conversation_Action;
DELETE FROM Conversation_Category;
DELETE FROM Conversation_Keyword;
DELETE FROM Conversation_Requirement;
DELETE FROM Conversation_Sentence;
DELETE FROM Conversation_Sentence_Action;
DELETE FROM Conversation_Sentence_Category_Has;
DELETE FROM Conversation_Sentence_Category_Set;
DELETE FROM Conversation_Sentence_Keyword;
DELETE FROM Conversation_Sentence_Requirement;


"""
