import pandas as pd
from pymongo import MongoClient
import os
from datetime import datetime

URI = "mongodb://Fostereum:.,Fostereum1433@ac-dzujpvu-shard-00-00.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-01.6jwnbo2.mongodb.net:27017,ac-dzujpvu-shard-00-02.6jwnbo2.mongodb.net:27017/?ssl=true&replicaSet=atlas-y8t6ay-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Fostereum"
DATABSE = "Fostereum"
COLLECTION = "sensor"
SAVE_PATH = "F:\Fostereum\devmode\dataset"
#-------------------------^ change to your drive
def get_next_filename(base_name, extension="csv"):
    save_directory = os.path.join(SAVE_PATH)
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    existing_files = [f for f in os.listdir(save_directory) if f.startswith(base_name) and f.endswith(extension)]
    if not existing_files:
        return os.path.join(save_directory, f"{base_name} 1.{extension}")
    numbers = [int(f.split(' ')[-1].split('.')[0]) for f in existing_files]
    next_number = max(numbers) + 1
    return os.path.join(save_directory, f"{base_name} {next_number}.{extension}")

client = MongoClient(URI)
db = client[DATABSE]
coll = db[COLLECTION]

data = [x for x in coll.find()]
df = pd.DataFrame.from_dict(data).drop("_id", axis=1)

today = datetime.now().strftime("%d-%m-%y")
base_name = f"{today} Dataset"
filename = get_next_filename(base_name)

df.to_csv(filename, index=False)
print(f"Dataset saved as {filename}")
