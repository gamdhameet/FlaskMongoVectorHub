from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Example knowledge base (replace with your own data)
knowledge_base = {
    "documents": [
        "Flask is a lightweight web framework for Python.",
        "GPT-4 is a state-of-the-art language model developed by OpenAI.",
        "Sentence transformers are used to generate embeddings for text.",
        "Vector databases are used to store and query high-dimensional vectors."
    ],
    "embeddings": None  # Will be populated on startup
}

# Precompute embeddings for the knowledge base
knowledge_base["embeddings"] = model.encode(knowledge_base["documents"])

@app.route('/embed', methods=['POST'])
def embed():
    """
    Endpoint to generate embeddings for input text.
    Expects a JSON payload with a "text" field.
    """
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Please provide 'text' in the request body"}), 400

    text = data['text']
    
    # Generate embeddings
    embeddings = model.encode(text)
    
    # Convert embeddings to a list (for JSON serialization)
    embeddings_list = embeddings.tolist()
    
    return jsonify({"embeddings": embeddings_list})

@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint to find the most relevant documents for a user query.
    Expects a JSON payload with a "query" field.
    """
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Please provide 'query' in the request body"}), 400

    query_text = data['query']
    
    # Generate embeddings for the query
    query_embedding = model.encode(query_text)
    
    # Compute similarity scores with the knowledge base
    similarity_scores = np.dot(knowledge_base["embeddings"], query_embedding)
    
    # Get the indices of the top 3 most relevant documents
    top_indices = np.argsort(similarity_scores)[-3:][::-1]
    
    # Prepare the results
    results = []
    for idx in top_indices:
        results.append({
            "document": knowledge_base["documents"][idx],
            "similarity_score": float(similarity_scores[idx])
        })
    
    return jsonify({"query": query_text, "results": results})

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)