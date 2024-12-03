from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from logs.logger import logging

# MongoDB client set-up
uri = "mongodb+srv://girmada:girmada@girmada.tuopq.mongodb.net/?retryWrites=true&w=majority&appName=Girmada"
logging.info("MongoDB URI is set")


client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
logging.info("Mongo Client set up is complete")

db = client["student_management"] # my database
logging.info(""""student_management" database set up is complete""")

students_collection = db["students"]  # my collection name
logging.info("""Collection set up by name - "students_collection" is complete""")


try:
    logging.info("Trying to ping the client...")
    client.admin.command('ping')
    logging.info("Successfully connected to MongoDB Atlas client")
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    logging.error("Could not connect to the client")
    print(e)


