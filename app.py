import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

# run this from the section5 file vs the code file bc the necessary code is in section5 .... use python code\app.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # SQLAlchemy database is going to live in the root folder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # turns off the flask SQLAlchemy modification tracker bc we are using the SQLAlchemy
                                                        # modification tracker (its being used as default and its better than the flask version)
app.secret_key = 'Thaddeus'
api = Api(app) # Api allows us to easily add resource

@app.before_first_request # removes the need to create_tables bc SQLAlchemy creates it for us
def create_tables():
    db.create_all() # only creates tables that it can see so be careful of to have everything imported

jwt = JWT(app, authenticate, identity) # creates a new endpoint /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # dont have to use decorator app.route() bc 2nd parameter takes care of it
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

db.init_app(app)

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug = True) # when an error occurs, the debug provides a helpful message
