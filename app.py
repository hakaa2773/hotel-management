from flask import Flask, request, redirect, render_template, jsonify
from pymongo import MongoClient
from bson import json_util
import requests

app = Flask(__name__)

client = MongoClient()
db = client["APIIT"]
collection = db.to_dos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hotel')
def hotel():
    return render_template('hotel.html')

@app.route('/search')
def search():

    recipe = request.args.get('a', 0, type=str)

    response = requests.get(f"http://www.recipepuppy.com/api/?q={recipe}")

    response = response.json()["results"][0]["title"]
    
    return jsonify(result=response)

@app.route('/foods')
def foods():

    recipe = request.args.get('a', 0, type=str)

    response = requests.get(f"http://www.recipepuppy.com/api/?q={recipe}")

    response = response.json()["results"][0]
    return render_template('foods.html', recipe=response)    

@app.route('/beer')
def beer():
    respones = requests.get(f"https://api.punkapi.com/v2/beers/random")
    random_beer_name=respones.json()[0]["name"]
    random_beer_description=respones.json()[0]["description"]
    return render_template('beer.html',title='beer', random_beer_name=random_beer_name, random_beer_description=random_beer_description)

@app.route('/traveling')
def travel():
    return render_template('travel.html')

@app.route('/view', methods=['GET'])
def get_todos():
    to_dos = list(collection.find())
    return json_util.dumps(to_dos)


@app.route('/add', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        new_todo = request.get_json()
        name = new_todo['name']
        description = new_todo['description']
        time = new_todo['time']

        collection.insert_one({
            "name": name, 
            "description": description,
            "time": time
        })
        return redirect('/view')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)

