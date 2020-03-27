import sqlite3
from db import db


# this user model here is an API (not a REST API) -> has 2 endpoints/methods, these two methods are an interface for the other parts of our program
# to interact w the user thing (including writing to a database and retrieving from a database)
class UserModel(db.Model): # not a resource, it's a helper -> helps store data about user and has some methods that allow us to retrieve user objects from a database
            # not a resource bc api cannot recieve data into this class or send this class as a json representation
            # user is a model: a model is our internal representation of an entity
            # a model is basically a helper that gives us more flexibility in our program without polluting the resource (resource is what the client interacts w)
            # resources are the external representation of an entity
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True) # telling SQLAlchemy that there's a column called id and its of type integer and
                                                # its the primary key (means it is unique and creates and index for it)
    username = db.Column(db.String(80)) # limits it to size of 80
    password = db.Column(db.String(80))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # find_by_username and find_by_id complete the mappings
        # allows us to retrieve a user by username/id and can do that w/ find_by_username and find_by_id

    @classmethod # not using self but are using the class name so its better to make it a class method
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # the orange username is the table name from where we are filtering
                                                              # (its the one listed on the very top of UserModel)
                                                              # the second one is the username argument

    @classmethod # not using self but are using the class name so its better to make it a class method
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

        connection.close() # don't have to commit bc didn't add any data
        return user # returning user object or None
