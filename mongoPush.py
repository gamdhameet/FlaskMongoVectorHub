import os
import json
from pymongo import MongoClient

# MongoDB Atlas configuration
MONGODB_URI = "mongodb+srv://sreevikramr:b9baMr-Rk-D_tm_@tamuhack25db.b2or5.mongodb.net/?retryWrites=true&w=majority&appName=tamuHack25DB"
DB_NAME = "tamuHack25DB"  # Replace with your database name
COLLECTION_NAME = "Teachers_RMP"  # Replace with your collection name
  
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://sreevikramr:b9baMr-Rk-D_tm_@tamuhack25db.b2or5.mongodb.net/?retryWrites=true&w=majority&appName=tamuHack25DB"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
def upload_json_to_mongodb():
    # Connect to MongoDB Atlas
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Process each JSON file in directory
    filename="Updated_Teacher_Reviews.json"
    file_path = os.path.join(filename)
    
    print(f"Processing {filename}...")
    
    try:
        with open(file_path, "r") as f:
            # Load JSON data
            data = json.load(f)
            
            # Insert documents into collection
            if isinstance(data, list):
                result = collection.insert_many(data)
                print(f"Inserted {len(result.inserted_ids)} documents")
            else:
                result = collection.insert_one(data)
                print(f"Inserted 1 document")
                
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

    client.close()
    print("Upload completed!")

if __name__ == "__main__":
    upload_json_to_mongodb()