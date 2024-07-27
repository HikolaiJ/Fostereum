from pymongo import MongoClient
import json

# MongoDB connection URI
uri = "mongodb://Fostereum:.,Fostereum1433@ac-dzujpvu-shard-00-00.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-01.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-02.6jwnbo2.mongodb.net:27017/?ssl=true&replicaSet=atlas-y8t6ay-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Fostereum"

# Connect to MongoDB
client = MongoClient(uri)
db = client['Fostereum']
collection = db['sensor']

# Test data
test_data = {
    "humidity": "humidity output",
    "temperature": "temperature output",
    "soilMoisture": "soilMoisture output",
    "mq135": "mq135 output"
}

# Insert data into MongoDB
result = collection.insert_one(test_data)

# Print the inserted ID
print(f"Data inserted with ID: {result.inserted_id}")
