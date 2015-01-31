from flask import current_app as app
from flask.ext.zodb import Object, List, Dict
from hashlib import sha256

class User():

	def __init__(self, username, password, userid):
		self.username = username
		self.passwordHash = sha256(password).hexdigest()
		self.id = userid
		self.restid_to_good_count = {}
		self.restid_to_bad_count = {}

	def updateGood(self, restid):
		if restid in self.restid_to_good_count:
			self.restid_to_good_count[restid] += 1
		else:
			self.restid_to_good_count[restid] = 1

	def updateBad(self, restid):
		if restid in self.rest_to_bad_count:
			self.restid_to_bad_count[restid] += 1
		else:
			self.restid_to_bad_count[restid] = 1


class Restaurant():
	'''
	#  name - string
	#  pos - (lat, lon) tuple of floats (in degrees)
	#  restid - int unique id for restaurant
	'''	
	def __init__(self, name, pos, restid):
		self.name = name
		self.lat = pos[0]
		self.lon = pos[1]
		self.id = restid
		self.goodCount = 0
		self.badCount = 0

	def updateGood(self):
		self.goodCount += 1

	def updateBad(self):
		self.badCount += 1
	
