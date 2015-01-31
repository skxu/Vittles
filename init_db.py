from ZODB.DB import DB
from ZODB.FileStorage import FileStorage
from flask.ext.zodb import Dict
import transaction

from models import User

first_user = User("Sam", "test1")

storage = FileStorage('app.fs')
conn = DB(storage)
db = conn.open().root()

if 'users' not in db:
	db['users'] = Dict()
	print('created users dict in db')

if 'restaurants' not in db:
	db['restaurants'] = Dict()
	print('created restaurants dict in db')

db['users'][first_user.id] = first_user

transaction.commit()
conn.close()