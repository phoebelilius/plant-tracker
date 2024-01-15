from pymongo import MongoClient
import os
from datetime import datetime

def mongodb_connection():
    try:
        username = os.environ["MONGODB_USERNAME"]
        password = os.environ["MONGODB_PASSWORD"]
        hostname = os.environ["MONGODB_HOSTNAME"]
        port = os.environ["MONGODB_PORT"]
        database = os.environ["MONGODB_DATABASE"]

        # if hostname empty, connect to localhost
        if hostname == "":
            hostname = "localhost"
        # if port empty, connect to 27017
        if port == "":
            port = "27017"
        # if database empty, connect to 'plant_database'
        if database == "":
            database = "plant_database"

        # if username and password empty, connect without authentication
        if username == "" and password == "":
            client = MongoClient(f"mongodb://{hostname}:{port}/{database}")
        else:
            client = MongoClient(f"mongodb://{username}:{password}@{hostname}:{port}/{database}")
        db = client[database]
        db.command("ping")  # Try a basic command to check the connection
        print("MongoDB connection successful.")
        return db

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)

def add_plant(db, name, species, watering_schedule):
    collection = db["plants"]
    plant_data = {
        "name": name,
        "species": species,
        "watering_schedule": watering_schedule,
        "last_watered": None,
    }
    result = collection.insert_one(plant_data)
    print(f"Plant added with ID: {result.inserted_id}")

def edit_plant(db, name, updates):
    collection = db["plants"]
    query = {"name": name}
    plant = collection.find_one(query)

    if plant:
        for key, value in updates.items():
            if value:  # Check if the input is not empty
                plant[key] = value

        result = collection.update_one({"_id": plant["_id"]}, {"$set": plant})
        print(f"Updated {result.modified_count} plant(s).")
    else:
        print(f"Plant not found with name: {name}")

def delete_plant(db, name):
    collection = db["plants"]
    result = collection.delete_one({"name": name})
    print(f"Deleted {result.deleted_count} plant(s).")

def water_plant(db, name):
    collection = db["plants"]
    query = {"name": name}
    update_time = {"$set": {"last_watered": datetime.now()}}
    result = collection.update_one(query, update_time)
    print(f"Watered {result.modified_count} plant(s).")

def format_time_difference(last_watered):
    now = datetime.now()
    time_difference = now - last_watered

    if time_difference.days > 0:
        return f"{time_difference.days} {'day' if time_difference.days == 1 else 'days'} ago"
    elif time_difference.seconds // 3600 > 0:
        return f"{time_difference.seconds // 3600} {'hour' if time_difference.seconds // 3600 == 1 else 'hours'} ago"
    else:
        return "Less than an hour ago"

def show_plants(db):
    collection = db["plants"]
    plants = collection.find()

    for plant in plants:
        last_watered = plant.get("last_watered")
        formatted_time_difference = format_time_difference(last_watered) if last_watered else "Never watered"
        print(f"Plant: {plant['name']}, Species: {plant['species']}, Watering Schedule: {plant['watering_schedule']}, Last Watered: {formatted_time_difference}")
