import json
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

# Load vectorized data
json_file_path = "USE THIS/tamu_architecture_filtered_data.json"
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Verify embedding dimensions
embedding_dim = len(data[0]["Embedding"])
print(f"Detected embedding dimension: {embedding_dim}")

# Load model matching your existing embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # Original 384-dim model
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")

# Prepare embeddings
embeddings = np.array([item["Embedding"] for item in data])
embeddings = normalize(embeddings)  # Normalize for cosine similarity

# Verify dimension match
if embeddings.shape[1] != 384:
    raise ValueError(f"Embedding dimension mismatch. Expected 384, got {embeddings.shape[1]}")

# Create NearestNeighbors index
nn_index = NearestNeighbors(n_neighbors=50, metric='cosine')
nn_index.fit(embeddings)

def search(query, top_n=3):
    # Encode query with same model used for embeddings
    query_vector = model.encode(query)
    query_vector = normalize([query_vector])
    
    # Nearest neighbors search
    distances, indices = nn_index.kneighbors(query_vector, return_distance=True)
    
    # Convert distances to similarities
    similarities = 1 - distances[0]
    
    # Cross-encoder re-ranking
    candidates = [(data[idx]["Specific Content"], similarities[i], idx) 
                 for i, idx in enumerate(indices[0])]
    cross_input = [[query, cand[0]] for cand in candidates]
    cross_scores = cross_encoder.predict(cross_input)
    
    # Combine and sort results
    combined = sorted(zip(indices[0], cross_scores), key=lambda x: x[1], reverse=True)
    top_indices = [item[0] for item in combined[:top_n]]
    
    # Display results
    print("\nSearch Results:\n")
    for idx in top_indices:
        print(f"Title: {data[idx]['Title']}")
        print(f"Content: {data[idx]['Specific Content'][:300]}...")
        print(f"URL: {data[idx]['URL']}")
        print(f"Confidence Score: {next(score for i, score in combined if i == idx):.4f}")
        print("-" * 80)

if __name__ == "__main__":
    while True:
        query = input("\nEnter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        search(query)