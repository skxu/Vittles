import flask
from yelp import Yelp
from flask import Flask
from flask import request
from flask.ext.restful import Resource, Api, reqparse
from flask.ext.zodb import ZODB, Dict
from models import User, Restaurant


yelp = Yelp()
app = Flask("Vittles")
app.config['ZODB_STORAGE'] = 'file://app.fs'

db = ZODB(app)

api = Api(app)




class Search(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('lon', required=True, type=float, help='Longitude(degrees) format example: lon=23.23')
		parser.add_argument('lat', required=True, type=float, help='Latitude(degrees) format example: lat=23.23')
		parser.add_argument('location', required=True, type=str, help="location='San Francisco'")
		args = parser.parse_args()

		#make call to yelp here
		data = yelp.search(args['lat'],args['lon'])
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

			return userid

class Restaurants(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('id', required=True, type=int)
		restid = parser.parse_args()['id']
		restaurant = db['restaurants'].get(restid, None)
		if restaurant != None:
			return {'name':restaurant.name}
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

			return restid
		

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
api.add_resource(Search, '/api/search')
api.add_resource(Register, '/api/users')
api.add_resource(Restaurants, '/api/restaurants')

app.run(debug=True, use_reloader=False)
