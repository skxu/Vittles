import json
import urllib
import urllib2
import oauth2

class Yelp():

	def __init__(self):
		self.YELP_BASE = "http://api.yelp.com/v2/"
		self.DEFAULT_LOCATION = 'San Francisco, CA'
		self.DEFAULT_TERM = 'food'

		self.CONSUMER_KEY = 'YOUR-KEY-HERE'
		self.CONSUMER_SECRET = 'YOUR-CONSUMER-SECRET-HERE'
		self.TOKEN = 'YOUR-TOKEN-HERE'
		self.TOKEN_SECRET = 'YOUR-TOKEN-SECRET-HERE'



	def search(self, lat, lon):
		params = {
				'term':self.DEFAULT_TERM,
				'location':self.DEFAULT_LOCATION,
				'cll':str(lat)+","+str(lon)
				}
		url = self.YELP_BASE+"search/"

		consumer = oauth2.Consumer(self.CONSUMER_KEY, self.CONSUMER_SECRET)
		oauth_request = oauth2.Request(method="GET",url=url, parameters=params)

		oauth_request.update(
			{
				'oauth_nonce': oauth2.generate_nonce(),
				'oauth_timestamp': oauth2.generate_timestamp(),
				'oauth_token': self.TOKEN,
				'oauth_consumer_key': self.CONSUMER_KEY
			}
		)

		token = oauth2.Token(self.TOKEN, self.TOKEN_SECRET)
		oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
		signed_url = oauth_request.to_url()

		print 'Querying {0} ...'.format(url)

		conn = urllib2.urlopen(signed_url, None)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()

		return response