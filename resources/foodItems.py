import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

foodItem = Blueprint('foodItems', 'foodItem')

@foodItem.route('/', methods=['GET'])
def get_all_foodItems():
	try:
		foodItems = [model_to_dict(foodItem) for foodItem in models.Food_item.select()]
		print(foodItems)
		return jsonify(data=foodItems, status={"code": 200, "message": "Success"})
	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})




@foodItem.route('/<id>/', methods=['PUT'])
def updated_foodItem(id):
	payload = request.get_json()
	foodItem_to_update = models.Food_item.get(id=id)

	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to edit foodItems'})

	if foodItem_to_update.creator.id is not current_user.id:
		return jsonify(data={}, status={'code': 401, 'message': 'You can only update foodItems you made'})

	foodItem_to_update.update(
		food_name=payload['food_name'],
		food_calories=payload['food_calories']
	).execute()

	update_foodItem_dict = model_to_dict(foodItem_to_update, max_depth=0)
	return jsonify(status={'code': 200, 'msg': 'success'}, data=update_foodItem_dict)




@foodItem.route('/', methods=['POST'])
def create_foodItem():
	payload = request.get_json()
	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a dog'})

	payload['creator'] = current_user.id
	foodItem = models.Food_item.create(**payload)
	foodItem_dict = model_to_dict(foodItem)
	return jsonify(data=foodItem_dict, status={"code": 201, "message": "Success"})



@foodItem.route('/<id>/', methods=["DELETE"])
def delete_foodItem(id):

	foodItem_to_delete = models.Food_item.get(id=id)

	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create foodItems'})
	if foodItem_to_delete.creator.id is not current_user.id:
		return jsonify(data={}, status={'code': 401, 'message': 'You can only delete foodItems you made'})
	foodItem_to_delete.delete()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})