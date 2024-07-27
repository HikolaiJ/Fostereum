from pymongo import MongoClient

# MongoDB connection URI
uri = "mongodb://Fostereum:.,Fostereum1433@ac-dzujpvu-shard-00-00.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-01.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-02.6jwnbo2.mongodb.net:27017/?ssl=true&replicaSet=atlas-y8t6ay-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Fostereum"

# Connect to MongoDB
client = MongoClient(uri)

# Select the database
db = client["Fostereum"]

# List and drop all collections in the database
collections = db.list_collection_names()
for collection_name in collections:
    print(f"Dropping collection: {collection_name}")
    db[collection_name].drop()

print("All collections have been cleared.")
