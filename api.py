import traceback
import flask
from yelp import Yelp
from flask import Flask
from flask import request
from flask.ext.restful import Resource, Api, reqparse
from flask.ext.zodb import ZODB, Dict
from models import User, Restaurant


from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()

yelp = Yelp()
app = Flask("Vittles")
app.config['ZODB_STORAGE'] = 'file://app.fs'

db = ZODB(app)

api = Api(app)



class Search(Resource):
	def get(self, userid):
		parser = reqparse.RequestParser()
		parser.add_argument('lon', required=True, type=float, help='Longitude(degrees) format example: lon=23.23')
		parser.add_argument('lat', required=True, type=float, help='Latitude(degrees) format example: lat=23.23')
		parser.add_argument('location', required=True, type=str, help="location='San Francisco'")
		args = parser.parse_args()

		data = None
		#make call to yelp here
		try:
			user = User.getUserById(db, userid)
			print("userid:", userid)
			if user == None:
				return {"message":"invalid userid"}, 400

			offset = user.getOffset()
			data = yelp.search(args['lat'],args['lon'], offset)
			restaurants = data['businesses']
			user.incrOffset(len(restaurants))
			User.save(db, user)
			for restaurant in restaurants:
				#parse yelp metadata
				name = restaurant['name']
				location = restaurant['location']
				lat = float(location['coordinate']['latitude'])
				lon = float(location['coordinate']['longitude'])
				pos = (lat, lon)
				if Restaurant.checkIfExists(db, pos):
					continue

				yelp_categories = restaurant['categories']
				categories = []
				for group in yelp_categories:
					categories.append(group[0]) #yelp format is [["Sam", "sam"], ["Blah","blah"]]

				address = location['address']
				city = location['city']
				zip_code = location['postal_code']
				yelp_rating = restaurant['rating']
				yelp_count = restaurant['review_count']
				img_url = restaurant['image_url']

				restid = db.get('restcount',0) + 1
				db['restcount'] = restid
				restObj = Restaurant(name, pos, restid, categories, yelp_count, yelp_rating, address, city, zip_code, img_url)

				Restaurant.save(db, restObj)

		except Exception as e:
			print traceback.format_exc()
		

		return data

class Register(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', required=True, type=str)
		parser.add_argument('password', required=True, type=str)
		args = parser.parse_args()
		
		username = args['username']
		if username in db['usernames']:
			return {'message':'username taken'}, 400
		else:
			
			db['usernames'].append(username)

			userid = db.get('usercount',0) + 1
			db['usercount'] = userid
			user = User(username, args['password'], userid)

			db['users'][userid] = user

			return {"userid":userid}

class Restaurants(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('id', required=True, type=int)
		restid = parser.parse_args()['id']
		restaurant = db['restaurants'].get(restid, None)
		if restaurant != None:
			return {
				'name':restaurant.name,
				'lat':restaurant.lat,
				'lon':restaurant.lon,
				'id':restaurant.id,
				'good_count':restaurant.good_count
				'bad_count':restaurant.bad_count
				'categories':restaurant.categories
				'yelp_count':restaurant.yelp_count
				'yelp_rating':restaurant.yelp_rating
				'address':restaurant.address
				'city':restaurant.city
				'zip_code':restaurant.zip_code
				'img_url':restaurant.img_url
			}
		else:
			return {'message':'restaurant id not found'}, 400

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', required=True, type=str)
		parser.add_argument('lat', required=True, type=float)
		parser.add_argument('lon', required=True, type=float)
		args = parser.parse_args()
		pos = (args['lat'],args['lon'])
		if pos in db['restaurants']:
			return {'message':'restaurant exists'}, 400
		else:
			restid = db.get('restcount',0) + 1
			db['restcount'] = restid
			restaurant = Restaurant(args['name'], pos, restid)
			db['restaurants'][pos] = restaurant		

			return {"restid":restid}
		

class UserAction(Resource):
	def post(self, userid):
		parser = reqparse.RequestParser()
		parser.add_argument('restid', required=True, type=int)
		parser.add_argument('liked', required=True, type=bool)
		args = parser.parse_args()

		restid = args['restid']
		#get User object
		user = db['users'].get(userid, None)
		if user == None:
			return {"message":"invalid userid"}, 400
		if args['liked']:
			user.updateGood(restid)
		else:
			user.updateBad(restid)

		db['users'][userid] = user
		return {"message":"200 OKAY"}


	def get(self, userid):
		user = db['users'].get(userid,None)
		if user == None:
			return {"message":"invalid userid"}, 400

		return {
			"restid_to_good_count":user.restid_to_good_count,
			"restid_to_bad_count":user.restid_to_bad_count
		}




api.add_resource(UserAction, '/api/users/<int:userid>/swipe')
api.add_resource(Search, '/api/search/<int:userid>')
api.add_resource(Register, '/api/users')
api.add_resource(Restaurants, '/api/restaurants')

app.run(debug=True, use_reloader=False)
