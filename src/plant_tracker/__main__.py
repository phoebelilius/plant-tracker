import argparse
import os
from datetime import datetime

from plant_tracker.db import Database
from plant_tracker.db.mongo import MongoDatabase


def format_time_difference(last_watered):
    now = datetime.now()
    time_difference = now - last_watered

    if time_difference.days > 0:
        return f"{time_difference.days} {'day' if time_difference.days == 1 else 'days'} ago"
    elif time_difference.seconds // 3600 > 0:
        return f"{time_difference.seconds // 3600} {'hour' if time_difference.seconds // 3600 == 1 else 'hours'} ago"
    else:
        return "Less than an hour ago"


def mongodb_connection():
    try:
        print("Connecting to MongoDB...")
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        hostname = os.getenv("MONGODB_HOSTNAME")
        port = os.getenv("MONGODB_PORT")
        database = os.getenv("MONGODB_DATABASE")

        # if hostname empty, connect to localhost
        if hostname is None:
            hostname = "localhost"
        # if port empty, connect to 27017
        if port is None:
            port = "27017"
        # if database empty, connect to 'plant_database'
        if database is None:
            database = "plant_database"

        # if username and password empty, connect without authentication
        if username is None and password is None:
            print(
                f"Connecting to MongoDB without authentication: mongodb://{hostname}:{port}/{database}"
            )
            client = MongoDatabase(
                f"mongodb://{hostname}:{port}/{database}", database, "plants"
            )
        else:
            print(
                f"Connecting to MongoDB with authentication: mongodb://{username}:{password}@{hostname}:{port}/{database}"
            )
            client = MongoDatabase(
                f"mongodb://{username}:{password}@{hostname}:{port}/{database}",
                database,
                "plants",
            )
        return client

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)


def main():
    # Ensure we are connected to the database
    db: Database = mongodb_connection()

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
