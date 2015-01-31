from ZODB.DB import DB
from ZODB.FileStorage import FileStorage
from flask.ext.zodb import Dict, List
import transaction

from models import User

storage = FileStorage('app.fs')
conn = DB(storage)
db = conn.open().root()

if 'users' not in db:
	db['users'] = Dict()
	print('created users dict in db')

if 'usernames' not in db:
	db['usernames'] = List()
	print('created usernames list in db')

if 'restaurants' not in db:
	db['restaurants'] = Dict()
	print('created restaurants dict in db')


transaction.commit()
conn.close()