#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

# TODO - This process runs as a cronjob and checks the sentence database
# for missing formal and informal versions of sentences.
# If one of the versions is missing it tries to transform the original version and informs the admin/trainer.
