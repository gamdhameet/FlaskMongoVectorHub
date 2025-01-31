from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

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
    
    # Return only the vectorized data
    return jsonify({"embeddings": embeddings_list})

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)