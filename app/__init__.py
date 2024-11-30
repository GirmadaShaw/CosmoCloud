from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB client set-up
uri = "mongodb+srv://girmada:girmada@girmada.tuopq.mongodb.net/?retryWrites=true&w=majority&appName=Girmada"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["student_management"] # my database
students_collection = db["students"]  # my collection name



