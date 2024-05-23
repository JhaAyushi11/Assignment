from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId, InvalidId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/assignment"
mongo = PyMongo(app)

movies_collection = mongo.db.movies

initial_data = [
    {
        "name": "Harry Potter and the Order of the Phoenix",
        "img": "https://bit.ly/2IcnSwz",
        "summary": "Harry Potter and Dumbledore's warning about the return of Lord Voldemort is not heeded by the wizard authorities who, in turn, look to undermine Dumbledore's authority at Hogwarts and discredit Harry."
    },
    {
        "name": "The Lord of the Rings: The Fellowship of the Ring",
        "img": "https://bit.ly/2tC1Lcg",
        "summary": "A young hobbit, Frodo, who has found the One Ring that belongs to the Dark Lord Sauron, begins his journey with eight companions to Mount Doom, the only place where it can be destroyed."
    },
    {
        "name": "Avengers: Endgame",
        "img": "https://bit.ly/2Pzczlb",
        "summary": "Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America, and Bruce Banner -- must figure out a way to bring back their vanquished allies for an epic showdown with Thanos -- the evil demigod who decimated the planet and the universe."
    }
]

if movies_collection.count_documents({}) == 0:
    movies_collection.insert_many(initial_data)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = []
    for movie in movies_collection.find():
        movie['_id'] = str(movie['_id'])
        movies.append(movie)
    return jsonify(movies), 200

@app.route('/movies', methods=['POST'])
def add_movie():
    new_movie = request.json
    movie_id = movies_collection.insert_one(new_movie).inserted_id
    new_movie['_id'] = str(movie_id)
    return jsonify(new_movie), 201

@app.route('/movies/<id>', methods=['GET'])
def get_movie(id):
    try:
        movie = movies_collection.find_one({"_id": ObjectId(id)})
        if movie:
            movie['_id'] = str(movie['_id'])
            return jsonify(movie), 200
        else:
            return jsonify({"error": "Movie not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid movie ID format"}), 400

@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    try:
        updated_data = request.json
        result = movies_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        if result.matched_count:
            updated_data['_id'] = id
            return jsonify(updated_data), 200
        else:
            return jsonify({"error": "Movie not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid movie ID format"}), 400

@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    try:
        result = movies_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Movie deleted"}), 200
        else:
            return jsonify({"error": "Movie not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid movie ID format"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
