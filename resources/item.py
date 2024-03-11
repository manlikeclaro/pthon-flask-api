import uuid

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
# from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

        # return {"items": list(items.values())}
        # return items.values()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError():
            abort(500, message="An error occurred during insertion")

        return item

        # for item in items.values():
        #     if (item_data['name'] == item['name']
        #             and item_data["store_id"] == item["store_id"]):
        #         abort(400, message='Item already exists!')

        # if item_data['store_id'] not in stores:
        #     # return {"error": "Store not found!"}, 404
        #     abort(404, message='Store not found!')

        # item_id = uuid.uuid4().hex
        # item = {**item_data, 'id': item_id}
        # items[item_id] = item
        # return item, 201


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        return item

        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message='Item not found!')

    @jwt_required()
    @blp.response(200)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"Message": "Item deleted!"}

        # try:
        #     del items[item_id]
        #     return {"message": "item deleted!"}
        # except KeyError:
        #     abort(404, message='Item not found!')

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

        # try:
        #     item = items[item_id]
        #     item |= item_data
        #     return item
        # except KeyError:
        #     abort(404, message="Item dos not exist!")
