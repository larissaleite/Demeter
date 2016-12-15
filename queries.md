The steps of the recommender are as follows:

#### Recommendation
1. Get all ratings from the database and pass on to Spark
2. Spark maps the ratings to RDD

##### If logged in user has rated at least one recipe
1. Spark verifies which recipes the logged in user hasn't yet rated so that it can predict the score for such recipes
2. Return a list of top 100 recipe_id ordered by score (descending)

##### If logged in user hasn't rated any recipes
1. Spark calculates the average rating for each recipe
2. Return a list of top 100 recipe_id ordered by average rating (descending)

#### Filtering
1. Get user's restricted ingredients and favorite recipes
2. For each ingredient in the restricted ingredients:
  * Get all recipes (recipe_id) that contain such ingredient and add to set of restricted recipes
3. Remove from the 100 recommended recipes, all the recipe\_id that are in the set of restricted recipes as well as the recipe_id in the user's favorite recipes

#### Boosting
1. Get user's preferred ingredients
2. For each recipe in the (filtered) recommended recipes list, get the names of the ingredients it contains
  * For each ingredient, if it is in the user's preferred ingredients list, increase the score of the recipe by 20%
3. Return a list of top 10 recipe_id ordered by score


Finally, after this, get title and image for each of the 10 recipes to be displayed to user.

### Data model

```
class Ingredient(EmbeddedDocument):
    name = StringField(max_length=255, required=True)
    meta = {'allow_inheritance': True}

#not necessary to inherit EmbeddedDocument again since Ingredient already does
class ExtendedIngredient(Ingredient):
    full_text = StringField(max_length=500)
    amount = IntField()
    unit = StringField(max_length=25)

class Review(EmbeddedDocument):
    ...

class Rating(Document):
    user = ReferenceField('User')
    recipe = ReferenceField('Recipe')
    rating = IntField(required=True)

class Recipe(Document):
    recipe_id = SequenceField()
    title = StringField(max_length=255, required=True)
    ingredients = ListField(EmbeddedDocumentField('ExtendedIngredient'))
    ...

class User(Document, UserMixin):
    ...
    user_id = SequenceField()
    preferred_ingredients = ListField(EmbeddedDocumentField('Ingredient'))
    allergies = ListField(EmbeddedDocumentField('Ingredient'))
    favorite_recipes = ListField(ReferenceField('Recipe'))```
