from db import db

class StoreModel(db.Model): # tell SQLAlchemy entity that this class are things we are going to be saving and retrieving from the database (create the mapping)

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True) # auto increments id so we don't have to do it ourself/ can do it ourself using unverisally unique id
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic') # establishes that there's a relationship w ItemModel -> is a list of ItemModels
                                                           # lazy = 'dynamic' turns it from a list to a query builder that has the ability to look into the items table
                                                           # does this bc it creates an object for each item in the database that matches the store_id which
                                                           # can be a lot if there's a lot of items


    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # .all() gives all the items in the item the items table

    @classmethod
    def find_by_name(cls, name): # should still be a class method bc it is going to return an object of type ItemModel rather than a dictionary
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name =name LIMIT 1; SQL does the connection,cursor etc for us

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self): # can update and insert data
        db.session.add(self) # session is the collection of objects that we are going to write to the database
        db.session.commit()
