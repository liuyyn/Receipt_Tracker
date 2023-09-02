from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
   # Get the env variables for username and password to connect to db
   USERNAME=os.getenv("USERNAME")
   PASSWORD=os.getenv("PASSWORD")
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.gqfwwui.mongodb.net/?retryWrites=true&w=majority"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)

   # Send a ping to confirm a successful connection
   try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
   except Exception as e:
      print(e)

   # Create the database for our example (we will use the same database throughout the tutorial
   return client.receipt

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   db = get_database()
   coll = db.receipt_info
   cursor = coll.find({})
   print(list(cursor))