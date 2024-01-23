import os
from datetime import datetime

from pymongo import MongoClient

from plant_tracker.db import Database


def get_connection_string():
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    hostname = os.getenv("MONGODB_HOSTNAME") or "localhost"
    port = os.getenv("MONGODB_PORT") or "27017"
    database = os.getenv("MONGODB_DATABASE")

    # connect with or without authentication
    mongo_connection_string = f"mongodb://{hostname}:{port}/{database}"
    if username is not None and password is not None:
        mongo_connection_string = (
            f"mongodb://{username}:{password}@{hostname}:{port}/{database}"
        )

    return mongo_connection_string


class MongoDatabase(Database):
    def __init__(
        self, db_name: str = "plant_database", collection_name: str = "plants"
    ):
        print("Connecting to MongoDB...")
        self._client = MongoClient(get_connection_string())
        self._db = self._client[db_name]
        self._plants = self._db[collection_name]
        # check if connection is successful
        try:
            print("Pinging MongoDB...")
            self._db.command("ping")
            print("MongoDB connection successful.")
        except Exception as e:
            print("MongoDB connection unsuccessful.")
            print(e)
            exit(1)

    def add_plant(self, name: str, species: str, watering_schedule: str):
        result = self._plants.insert_one(
            {
                "name": name,
                "species": species,
                "watering_schedule": watering_schedule,
                "last_watered": None,
            }
        )
        print(f"Plant added with ID: {result.inserted_id}")

    def edit_plant(self, name: str, updates: dict):
        plant = self._plants.find_one({"name": name})

        if plant:
            for key, value in updates.items():
                if value:  # Check if the input is not empty
                    plant[key] = value

            result = self._plants.update_one({"_id": plant["_id"]}, {"$set": plant})
            print(f"Updated {result.modified_count} plant(s).")
        else:
            print("No matching plant found.")

    def delete_plant(self, name: str):
        result = self._plants.delete_one({"name": name})
        print(f"Deleted {result.deleted_count} plant(s).")

    def water_plant(self, name: str):
        plant = self._plants.find_one({"name": name})

        if plant:
            plant["last_watered"] = datetime.now()
            result = self._plants.update_one({"_id": plant["_id"]}, {"$set": plant})
            print(f"Watered {result.modified_count} plant(s).")
        else:
            print("No matching plant found.")

    def get_plants(self):
        return self._plants.find()
