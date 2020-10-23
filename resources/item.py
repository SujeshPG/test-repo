from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This is required")
    parser.add_argument('store_id',type=int,required=True,help="This is required")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"message":"Item not found"},400


    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message": "This item name already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured in inserting"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message":"Item deleted"}

    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        return {'items' :[item.json() for item in ItemModel.query.all()]}
        ''' we can also use lambda like:
            return {'items' : list(map(lambda x: x.json(),ItemModel.query.all()))}'''