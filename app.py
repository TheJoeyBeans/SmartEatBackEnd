from flask import Flask, g, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager
from playhouse.shortcuts import model_to_dict
from resources.meals import meal
from resources.foodItems import foodItem
from resources.users import user
import os
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)


app.secret_key = 'Shhheeeee, secret key yo'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

CORS(meal, origins=['http://localhost:3000', 'https://smart-eat.herokuapp.com'], supports_credentials=True)
app.register_blueprint(meal, url_prefix='/api/v1/meals')

CORS(foodItem, origins=['http://localhost:3000', 'https://smart-eat.herokuapp.com'], supports_credentials=True)
app.register_blueprint(foodItem, url_prefix='/api/v1/foodItems')

CORS(user, origins=['http://localhost:3000', 'https://smart-eat.herokuapp.com'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/user')

if 'ON_HEROKU' in os.environ:
	print('hitting ')
	models.initialize()

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

