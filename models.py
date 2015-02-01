from flask import current_app as app
from flask.ext.zodb import Object, List, Dict, ZODB
from hashlib import sha256

class User():

	def __init__(self, username, password, userid):
		self.username = username
		self.passwordHash = sha256(password).hexdigest()
		self.id = userid
		self.offset = 0
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

	def clearOffset(self):
		self.offset = 0

	def incrOffset(self, amount):
		self.offset += amount

	def getOffset(self):
		return self.offset

	@staticmethod
	def getUserById(db, userid):
		user = db['users'].get(userid, None)
		return user

	@staticmethod
	def save(db, user):
		print("updating user with id:"+str(user.id))
		db['users'][user.id] = user


class Restaurant():
	'''
	#  @name - string
	#  @pos - (lat, lon) tuple of floats (in degrees)
	#  @restid - int unique id for restaurant
	#  @categories - [str1, str2, str3, ...]
	#  @yelpCount - int
	#  @yelpRating - float
	#  @address - str
	#  @city - str
	#  @streets - str
	#  @zip_code - str
	'''	
	def __init__(self, name, pos, restid, categories, yelp_count, yelp_rating, address, city, zip_code, img_url):
		self.name = name
		self.pos = pos
		self.lat = pos[0]
		self.lon = pos[1]
		self.id = restid
		self.goodCount = 0
		self.badCount = 0

		#yelp metadata
		self.categories = categories
		self.yelp_count = yelp_count
		self.yelp_rating = yelp_rating
		self.address = address
		self.city = city
		self.zip_code = zip_code
		self.img_url = img_url


	def updateGood(self):
		self.goodCount += 1

	def updateBad(self):
		self.badCount += 1

	#db - flask-ZODB instance
	@staticmethod
	def checkIfExists(db, pos):
		if pos in db['restaurants']:
			return True
		else:
			return False

	@staticmethod
	def getByPos(db, pos):
		return db['restaurants'].get(pos, None)

	@staticmethod
	def save(db, restObj):
		db['restaurants'][restObj.pos] = restObj
		print "added "+restObj.name+" to the db."



	
