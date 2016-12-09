import datetime
from flask_login import UserMixin
from mongoengine import *

class Ingredient(EmbeddedDocument):
	name = StringField(max_length=255, required=True)
	meta = {'allow_inheritance': True}

#not necessary to inherit EmbeddedDocument again since Ingredient already does
class ExtendedIngredient(Ingredient):
	full_text = StringField(max_length=500)
	amount = IntField()
	unit = StringField(max_length=25)
	category = StringField(max_length=50) #just for spoonacular

class Review(EmbeddedDocument):
	id = StringField(max_length=500, required=True)
	text = StringField(max_length=500, required=True)
	user = ReferenceField('User')
	recipe = ReferenceField('Recipe')
	date = DateTimeField(default=datetime.datetime.now, required=True)

class Rating(Document):
	user = ReferenceField('User')
	recipe = ReferenceField('Recipe')
	rating = IntField(required=True)

class Recipe(Document):
	recipe_id = SequenceField()
	title = StringField(max_length=255, required=True)
	ingredients = ListField(EmbeddedDocumentField('ExtendedIngredient'))
	image = StringField(max_length=255)
	instructions = StringField(max_length=500)
	vegetarian = BooleanField()
	vegan = BooleanField()
	glutenFree = BooleanField()
	dairyFree = BooleanField()
	fatFree = BooleanField()
	peanutFree = BooleanField()
	calories = FloatField()
	reviews = ListField(EmbeddedDocumentField('Review'))

class User(Document, UserMixin):
	first_name = StringField(max_length=255, required=True)
	last_name = StringField(max_length=255, required=True)
	fb_id = IntField(required=True)
	fb_token = StringField(max_length=255, required=True)
	age = IntField()
	gender = BinaryField()
	email = StringField(max_length=255)
	location = StringField(max_length=255)
	coordinates = StringField(max_length=255)
	preferred_ingredients = ListField(EmbeddedDocumentField('Ingredient'))
	allergies = ListField(EmbeddedDocumentField('Ingredient'))
	diet_labels = ListField(StringField(max_length=50))
	favorite_recipes = ListField(ReferenceField('Recipe'))
