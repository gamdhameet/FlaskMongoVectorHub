from flask import Flask, request, jsonify
from pymongo import MongoClient
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.preprocessing import normalize

# Flask App
app = Flask(__name__)

# MongoDB Atlas Connection
MONGODB_URI = "mongodb+srv://sreevikramr:b9baMr-Rk-D_tm_@tamuhack25db.b2or5.mongodb.net/?retryWrites=true&w=majority&appName=tamuHack25DB"
DB_NAME = "tamuHack25DB"  # Replace with your database name
COLLECTION_NAME = "Teachers_RMP"  # Replace with your collection name  
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]  # Collection where vector embeddings are stored

# Load models
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    top_n = int(request.args.get("top_n", 10))

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Encode the query into a 384-dimensional vector
    query_vector = model.encode(query)
    query_vector = normalize([query_vector])[0].tolist()  # Convert to list for MongoDB

    # Perform Vector Search in MongoDB Atlas
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",  # Ensure this matches your MongoDB Atlas vector index name
                "path": "Embedding",
                "queryVector": query_vector,
                "numCandidates": 100,  # Retrieve top 100 candidates before filtering
                "limit": top_n
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    if not results:
        return jsonify({"message": "No relevant documents found."})

    # Format response
    response = []
    for doc in results:
        response.append({
            "Name": doc["Name"],
            "comment": doc["comment"],
            "Attendance Mandatory": doc["attendanceMandatory"],
            "Rating": doc["clarityRating"],
            "Helpfulness": doc["helpfulRating"],
            "Difficulty": doc["difficultyRating"],
            "ratingTags": doc["ratingTags"],
        })

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)