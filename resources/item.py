from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource): # resource are all classes, resource is used to map endpoints such as HTTP verbs to the '/item/name'
    parser = reqparse.RequestParser()       # replaces request.get_json since it forces the user to enter a certain argument
    parser.add_argument('price',            # in this case, the argument is 'price'
    type = float,
    required = True,
    help = 'This field cannot be left blank'
    )
    parser.add_argument('store_id',
    type = int,
    required = True,
    help = 'Every item needs a store id'
    )

    @jwt_required()
    def get(self,name): # not called by api directly, only used within the code (it should be moved to model)
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "there was an error getting the item"}, 500
        if item:
            return item.json()
        return {"message": "Item not found"}, 404


    @jwt_required()
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': 'item already exists'}, 400
        data = Item.parser.parse_args()

               # data = request.get_json() - > must set the Content type in postman properly (force=True in get_jston parameter prevents this error)/
               # body must be in Json or this line will return an error (silent = True makes get_json return null if there's an error)
        print(data)
        item = ItemModel(name, data['price'], data['store_id'])

        try:                                            # /item/<string:name>, that will become the name parameter (we receive information through
            item.save_to_db()                       # the URL so these all these things can be accessed by the same endpoint just by changing the HTTP verb)
        except:
            return {"message": "there was an error inserting the item"}, 500
        return item.json(), 201                          # tells the client such as Postman that we have processed this addition
                                                  # Status code: 201 (CREATED), 202 (ACCEPTED): use this when delaying a creation
    @jwt_required()
    def delete (self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'Message': 'Item deleted'}

    @jwt_required() # requires you to authenticate before using this method (put())
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)  # **data = data['price'], data['store_id']
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} # returns all in the database, use list(map(...)) when working w others using other
                                                                    # languages bc easier to understand
