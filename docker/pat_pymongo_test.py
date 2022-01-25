import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:5000/")
mydb = myclient["HearthstoneDB"]
mycol = mydb["replaysTest"]

mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)