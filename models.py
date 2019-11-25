import os
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect


DATABASE = connect(os.environ.get('DATABASE_URL'))

class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField()

	def __str__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	def __repr__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	class Meta:
		db_table = 'users'
		database = DATABASE

class Meal(Model):
	meal_type = CharField()
	calories = IntegerField()
	creator = ForeignKeyField(User, related_name='meals')

	class Meta: 
		db_table = 'meals'
		database = DATABASE

class Food_item(Model):
	food_name = CharField()
	food_calories = IntegerField()
	food_unique_id = CharField()
	meal = ForeignKeyField(Meal, backref='food_items')
	creator = ForeignKeyField(User, related_name='FoodItems')

	class Meta:
		db_table = 'food_items'
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Meal, Food_item], safe=True)
	print('TABLES Created')
	DATABASE.close()
