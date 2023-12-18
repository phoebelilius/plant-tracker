# plant_tracker/main.py
from plant_tracker.db import mongodb_connection, add_plant, edit_plant, delete_plant, water_plant, show_plants
import argparse

def main():
    db = mongodb_connection()  # Call once at startup

    parser = argparse.ArgumentParser(description="Plant Tracking CLI App")
    parser.add_argument("command", choices=["add", "edit", "delete", "show", "water"], help="Operation to perform")

    args = parser.parse_args()

    if args.command == "add":
        name = input("Enter plant name: ")
        species = input("Enter plant species: ")
        watering_schedule = input("Enter watering schedule: ")
        add_plant(db, name, species, watering_schedule)
    elif args.command == "edit":
        name = input("Enter plant name to edit: ")
        updates = {
            "species": input("Enter new species (leave blank to keep existing): "),
            "watering_schedule": input("Enter new watering schedule (leave blank to keep existing): "),
        }
        edit_plant(db, name, updates)
    elif args.command == "delete":
        name = input("Enter plant name to delete: ")
        delete_plant(db, name)
    elif args.command == "show":
        show_plants(db)
    elif args.command == "water":
        name = input("Enter plant name to water: ")
        water_plant(db, name)

if __name__ == "__main__":
    main()
