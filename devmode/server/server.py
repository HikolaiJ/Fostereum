from flask import Flask, request, jsonify
from pymongo import MongoClient
print("===FOSTEREUM===")
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://Fostereum:.,Fostereum1433@ac-dzujpvu-shard-00-00.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-01.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-02.6jwnbo2.mongodb.net:27017/?ssl=true&replicaSet=atlas-y8t6ay-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Fostereum")
db = client['Fostereum']
collection = db['sensor']

@app.route('/sensor_data', methods=['POST'])
def sensor_data():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Sensor data received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
