import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

foodItem = Blueprint('foodItems', 'foodItem')

# GET ROUTE FOR FOOD ITEMS
@foodItem.route('/', methods=['GET'])
def get_all_foodItems():
	try:
		foodItems = [model_to_dict(foodItem) for foodItem in models.Food_item.select()]
		print(foodItems)
		return jsonify(data=foodItems, status={"code": 200, "message": "Success"})
	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# EDIT ROUTE FOR FOOD ITEMS
@foodItem.route('/<id>/', methods=['PUT'])
def updated_foodItem(id):
	payload = request.get_json()
	query = models.Food_item.update(**payload).where(models.Food_item.id==id)

	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to edit foodItems'})

	query.execute()
	return jsonify(status={'code': 200, 'msg': 'success'}, data=model_to_dict(models.Food_item.get_by_id(id)))



# CREATE ROUTE FOR FOODITEMS
@foodItem.route('/', methods=['POST'])
def create_foodItem():
	payload = request.get_json()
	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a foodItem'})

	payload['creator'] = current_user.id
	foodItem = models.Food_item.create(**payload)
	foodItem_dict = model_to_dict(foodItem)
	return jsonify(data=foodItem_dict, status={"code": 201, "message": "Success"})


# DELETE ROUTE FOR FOODITEMS
@foodItem.route('/<id>/', methods=["DELETE"])
def delete_foodItem(id):

	foodItem_to_delete = models.Food_item.get(id=id)

	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create foodItems'})
	if foodItem_to_delete.creator.id is not current_user.id:
		return jsonify(data={}, status={'code': 401, 'message': 'You can only delete foodItems you made'})
	query = foodItem_to_delete.delete().where(models.Food_item.id==id)
	query.execute()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})