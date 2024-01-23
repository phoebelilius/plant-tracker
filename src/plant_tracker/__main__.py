import argparse

from plant_tracker.common import format_time_difference
from plant_tracker.db import Database
from plant_tracker.db.mongo import MongoDatabase


def main():
    # Ensure we are connected to the database
    db: Database = MongoDatabase()

    parser = argparse.ArgumentParser(description="Plant Tracking CLI App")
    parser.add_argument(
        "command",
        choices=["add", "edit", "delete", "show", "water"],
        help="Operation to perform",
    )

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
            "watering_schedule": input(
                "Enter new watering schedule (leave blank to keep existing): "
            ),
        }
        db.edit_plant(name, updates)
    elif args.command == "delete":
        name = input("Enter plant name to delete: ")
        db.delete_plant(name)
    elif args.command == "show":
        print("All plants:")
        for plant in db.get_plants():
            last_watered = plant.get("last_watered")
            formatted_time_difference = (
                format_time_difference(last_watered)
                if last_watered
                else "Never watered"
            )
            print(
                f"Plant: {plant['name']}, Species: {plant['species']}, Watering Schedule: {plant['watering_schedule']}, Last Watered: {formatted_time_difference}"
            )

    elif args.command == "water":
        name = input("Enter plant name to water: ")
        db.water_plant(name)


if __name__ == "__main__":
    main()
