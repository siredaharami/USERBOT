# db.py
from pymongo import MongoClient

# MongoDB connection URI (replace with your actual connection URI)
MONGO_URI = "mongodb://localhost:27017/"  # Update this if using a cloud database like MongoDB Atlas

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select the database
db = client["userbot"]  # You can change the name of the database if needed

# Select the collection
users_collection = db["users"]  # This will store user PM security and message count data

# Function to get user data
def get_user_data(user_id):
    user_data = users_collection.find_one({"user_id": user_id})
    if user_data:
        return user_data
    else:
        return None

# Function to update user data
def update_user_data(user_id, pm_level, messages_sent, last_message_time):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"pm_level": pm_level, "messages_sent": messages_sent, "last_message_time": last_message_time}},
        upsert=True
    )
