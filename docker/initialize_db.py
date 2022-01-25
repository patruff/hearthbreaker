from pymongo import Connection
connection = Connection()
db = connection['HearthstoneDB']
collection = db['testReplays2']