import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
# from db import stores
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("stores", __name__, description="operations on stores")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

        # return {"stores": list(stores.values())}
        # return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError():
            abort(400, message="A store with similar name exists!")
        except SQLAlchemyError():
            abort(500, message="Error occurred creating store!")

        return store

        # for store in stores.values():
        #     if store_data['name'] == store['name']:
        #         abort(400, message='Store already exists!')
        #
        # store_id = uuid.uuid4().hex
        # store = {**store_data, 'id': store_id}
        # stores[store_id] = store
        # return store, 201


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

        # store = stores.get(store_id)
        # if store is None:
        #     abort(404, message='Store not found!')
        #
        # return store

        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message='Store not found!')

    @blp.response(200)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"Message": "Store deleted!"}

        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted!"}
        # except KeyError:
        #     abort(404, message="Store doesnt exist")

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)

        if store:
            store.name = store_data["name"]
        else:
            item = StoreModel(id=store_id, **store_data)

        db.session.add(store)
        db.session.commit()

        return store

        # try:
        #     store = stores[store_id]
        #     store |= store_data
        #     return store
        # except KeyError:
        #     abort(404, message="Store does not exist!")
