import pandas as pd
from sentence_transformers import SentenceTransformer
import json

# Load the CSV file
file_list = [
    "Updated_Teacher_Reviews.csv"
]
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
for file_path in file_list:
     # Update this path if needed
    print("Reading CSV file..."+file_path)
    df = pd.read_csv(f"{file_path}")
    print("CSV file read successfully")
    # Vectorize the "Specific Content" column and ensure embeddings are stored as lists
    df["Embedding"] = df["Name"].astype(str).apply(lambda x: model.encode(x).tolist())
    
    # Prepare data for JSON storage
    json_data = df.to_dict(orient="records")
    
    # Save to JSON file
    json_file_path = f"{file_path.split('.')[0]}.json"
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    
    print(f"Vectorized data saved to {json_file_path}")