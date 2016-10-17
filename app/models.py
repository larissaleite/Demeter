import datetime
from flask_login import UserMixin
from mongoengine import *

class Category(EmbeddedDocument):
	category = StringField(max_length=100, required=True)

class Ingredient(EmbeddedDocument):
	name = StringField(max_length=255, required=True)
	category = ReferenceField('Category')
	meta = {'allow_inheritance': True}

#not necessary to inherit EmbeddedDocument again since Ingredient already does
class ExtendedIngredient(Ingredient):
	amount = IntField(required=True)
	unit = StringField(max_length=25, required=True)

class Review(EmbeddedDocument):
	text = StringField(max_length=500, required=True)
	user = ReferenceField('User')
	recipe = ReferenceField('Recipe')
	date = DateTimeField(default=datetime.datetime.now, required=True)

class Rating(EmbeddedDocument):
	user = ReferenceField('User')
	recipe = ReferenceField('Recipe')
	rate = IntField(required=True)

class Recipe(Document):
	title = StringField(max_length=255, required=True)
	ingredients = ListField(EmbeddedDocumentField('ExtendedIngredient'))
	image = StringField(max_length=100)
	instructions = StringField(max_length=500)
	vegetarian = BooleanField(required=True)
	vegan = BooleanField(required=True)
	glutenFree = BooleanField(required=True)
	dairyFree = BooleanField(required=True)

class User(Document, UserMixin):
	first_name = StringField(max_length=255, required=True)
	last_name = StringField(max_length=255, required=True)
	fb_id = IntField(required=True)
	fb_token = StringField(max_length=255, required=True)
	age = IntField()
	gender = BinaryField()
	email = StringField(max_length=255)
	location = StringField(max_length=255)
	preferred_ingredients = ListField(EmbeddedDocumentField('Ingredient'))
	allergies = ListField(EmbeddedDocumentField('Ingredient'))
	favorite_recipes = ListField(ReferenceField('Recipe'))
