# plant_tracker/main.py
from dbv2 import Database
from db_mongo import MongoDatabase
import argparse


def main():
    # Ensure we are connected to the database
    db: Database = MongoDatabase("mongodb://localhost:27017/")

    parser = argparse.ArgumentParser(description="Plant Tracking CLI App")
    parser.add_argument("command", choices=["add", "edit", "delete", "show", "water"], help="Operation to perform")

    args = parser.parse_args()

    if args.command == "add":
        name = input("Enter plant name: ")
        species = input("Enter plant species: ")
        watering_schedule = input("Enter watering schedule: ")
        db.add_plant(name, species, watering_schedule)
    elif args.command == "edit":
        name = input("Enter plant name to edit: ")
        updates = {
            "species": input("Enter new species (leave blank to keep existing): "),
            "watering_schedule": input("Enter new watering schedule (leave blank to keep existing): "),
        }
        db.edit_plant(name, updates)
    elif args.command == "delete":
        name = input("Enter plant name to delete: ")
        db.delete_plant(name)
    elif args.command == "show":
        db.get_plants()
    elif args.command == "water":
        name = input("Enter plant name to water: ")
        db.water_plant(name)

if __name__ == "__main__":
    main()
