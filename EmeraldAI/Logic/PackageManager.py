#!/usr/bin/python
# -*- coding: utf-8 -*-
import pip
import imp

class PackageManager(object):
	def Install(package):
		try:
			pip.main(['install', package])
			return True
		except:
			return False

	def Upgrade(package):
		try:
			pip.main(['install', '--upgrade', package])
			return True
		except:
			return False

	def IsAvailable(package):
		try:
			imp.find_module('aiml')
			return True
		except ImportError:
			return False
