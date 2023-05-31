
from flask import Flask, request, jsonify, render_template
import pandas as pd
from model import enrichir
import json
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://goulag:9eKA5GfkeqbTTEu8@cluster5.2qw5j.mongodb.net/Goulag?retryWrites=true&w=majority")
db = client["Goulag"]

# récupérer une référence à la collection contenant les profils
profils_collection = db["profiles"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get("occupations")
    occupation = text.split('.')
    print(occupation)
    output = enrichir(occupation, 1000)

    return render_template('index.html', prediction_text=output)

@app.route('/retrieve_ids', methods=['POST'])
def retrieve_ids():
    # Étape 1: Récupérez les identifiants à partir du formulaire POST
    ids_string = request.form['ids']
    ids = json.loads(ids_string)

    # Étape 2: Récupérez les utilisateurs de la base de données MongoDB en utilisant les identifiants
    retrieved_users = profils_collection.find({"_id": {"$in": [ObjectId(user_id) for user_id in ids]}})

    # Étape 3: Pas besoin d'appeler la fonction enrichir ici

    # Étape 4: Passez la liste des utilisateurs à la fonction render_template
    return render_template('results.html', users=retrieved_users)


@app.route('/results', methods=['POST'])
def results():
    if request.method == 'GET':
        return jsonify({"error": "Please send a JSON object with the 'occupations' key in the request body"}), 400

    try:
        data = request.get_json(force=True)
        occupation = data.get("occupations")
        count = data.get("count")
        print(occupation)
        output = enrichir(occupation, count)

        return jsonify(output)
    except ValueError as e:
        return jsonify({"error": "Invalid JSON object", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
