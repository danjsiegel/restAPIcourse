from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'price', 
		type=float, 
		required=True, 
		help="This field cannot be blank"
	)
	parser.add_argument(
		'store_id', 
		type=int, 
		required=True, 
		help="Every store needs an id"
	)
	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {"message":"No such item"}, 404
	
	def post(self, name):
		if ItemModel.find_by_name(name):
			return{"message": "An item with name {} already exists".format(name)}, 400
		post_data = Item.parser.parse_args()
		item = ItemModel(name, **post_data)
		
		try:
			item.save_to_db()
		except:
			return {"message":"an error occured inserting the item"}, 500
		
		return item.json(), 201

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {"message":"Item Deleted"}
		
	def put(self, name):
		post_data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			try:
				item = ItemModel(name, post_data['price'], post_data['store_id'])
			except:
				return {"message":"an error occured while inserting item"}, 500
		else:
			try:
				item.price = post_data['price']
			except:
				return {"message":"an error occured while inserting item"}, 500
		
		item.save_to_db()
		
		return item.json(), 200


class ItemList(Resource):
	def get(self):
		return {"items":list(map(lambda x: x.json(), ItemModel.query.all()))}
