# import relevant modules
from pymongo import MongoClient

client = MongoClient(port=27017)
db = client.train_data

col = db.traindelays


for x in col.find():
    print(x)
