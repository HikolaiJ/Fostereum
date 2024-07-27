from pymongo import MongoClient

uri = "mongodb://Fostereum:.,Fostereum1433@ac-dzujpvu-shard-00-00.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-01.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-02.6jwnbo2.mongodb.net:27017/?ssl=true&replicaSet=atlas-y8t6ay-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Fostereum"
try:
    client = MongoClient(uri)
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"An error occurred: {e}")
