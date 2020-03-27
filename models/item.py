from db import db

class ItemModel(db.Model): # tell SQLAlchemy entity that this class are things we are going to be saving and retrieving from the database (create the mapping)

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True) # auto increments id so we don't have to do it ourself/ can do it ourself using unverisally unique id
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # foreign key links store_id from ItemModel to stores.id from stores
    store = db.relationship('StoreModel') # establishes there's only 1 store w all the items w same store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name): # should still be a class method bc it is going to return an object of type ItemModel rather than a dictionary
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name =name LIMIT 1; SQL does the connection,cursor etc for us

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self): # can update and insert data
        db.session.add(self) # session is the collection of objects that we are going to write to the database
        db.session.commit()
