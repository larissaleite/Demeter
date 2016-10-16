from flask import Flask, render_template, jsonify, make_response, request, flash
import requests

app = Flask(__name__)

headers = {
    "X-Mashape-Key": "62t27Bg1q7mshtmPnpbNVMOAVw9Tp1PkKrqjsnebv8Ph00q2x3",
    "Accept": "application/json"
}

@app.route('/', methods=['GET'])
def index():
    response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=false&number=1", headers=headers)
    data = response.json()

    recipes = []

    for recipe in data['recipes']:
        recipes.append({ 'title' : recipe['title'], 'img' : recipe['image'], 'instructions' : recipe['instructions'] })

    return render_template("index.html", recipes=recipes)

if __name__ == '__main__':
	app.secret_key = 'secret key'
	from os import environ
	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)), processes=1)
