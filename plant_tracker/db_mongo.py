from pymongo import MongoClient
from dbv2 import Database
from datetime import datetime


class MongoDatabase(Database):
    def __init__(self, mongo_connection_str: str):
        self._client = MongoClient(mongo_connection_str)
        self._db = self._client["plant_database"]
        self._plants = self._db["plants"]
        # check if connection is successful
        self._db.command("ping")
        print("MongoDB connection successful.")

    def add_plant(self, name: str, species: str, watering_schedule: str):
        result = self._plants.insert_one({
            "name": name,
            "species": species,
            "watering_schedule": watering_schedule,
            "last_watered": None,
        })
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
