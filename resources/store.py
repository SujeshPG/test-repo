from flask_restful import Resource,reqparse

from models.store import StoreModel

class Store(Resource):

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'store not found'},404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message':'Store already exist'}, 400
        store = StoreModel(name)
        
        try:
            store.save_to_db()
        except:
            return {'message':'error occured'}, 500
        
        return store.json(),201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':'store closed'}


class StoreList(Resource):
    def get(self):
        return {'store': [store.json() for store in StoreModel.query.all()]}