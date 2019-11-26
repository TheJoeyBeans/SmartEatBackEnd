import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

meal = Blueprint('meals', 'meal')

@meal.route('/', methods=["GET"])
def get_all_meals():
	try:
		meals = [model_to_dict(meal) for meal in models.Meal.select()]
		print(meals)
		return jsonify(data=meals, status={"code": 200, "message": "Success"})
	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})




@meal.route('/<id>/', methods=['PUT'])
def updated_meal(id):
	payload = request.get_json()
	meal_to_update = models.Meal.get(id=id)

	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to edit a meal'})

	if meal_to_update.creator.id is not current_user.id:
		return jsonify(data={}, status={'code': 401, 'message': 'You can only update meals you made'})

	meal_to_update.update(
		meal_type=payload['meal_type'],
		calories=payload['calories']
	).execute()

	update_meal_dict = model_to_dict(meal_to_update, max_depth=0)
	return jsonify(status={'code': 200, 'msg': 'success'}, data=update_meal_dict)




@meal.route('/', methods=['POST'])
def create_meal():
	payload = request.get_json()
	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a meal'})
	
	payload['creator'] = current_user.id
	meal = models.Meal.create(**payload)
	meal_dict = model_to_dict(meal)
	return jsonify(data=meal_dict, status={"code": 201, "message": "Success"})




@meal.route('/<id>/', methods=["DELETE"])
def delete_meal(id):
	meal_to_delete = models.Meal.get(id=id)
	print(model_to_dict(meal_to_delete))
	query = meal_to_delete.delete().where(models.Meal.id==id)
	query.execute()
	return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})


