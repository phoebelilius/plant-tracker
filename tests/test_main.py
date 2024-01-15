# tests/test_main.py
import unittest
from unittest.mock import patch
from pymongo import MongoClient
from plant_tracker.db.db import add_plant, edit_plant, delete_plant, water_plant


class TestPlantTracker(unittest.TestCase):
    def setUp(self):
        # Create a test MongoDB database for testing
        self.test_client = MongoClient()
        self.test_db = self.test_client["test_plant_database"]

    def tearDown(self):
        # Clean up after each test by dropping the test database
        self.test_client.drop_database("test_plant_database")

    @patch("builtins.input", side_effect=["John", "Rose", "Twice a week"])
    def test_add_plant(self, mock_input):
        db = self.test_db
        add_plant(db, "John", "Rose", "Twice a week")
        plant = db["plants"].find_one({"name": "John"})
        self.assertIsNotNone(plant)
        self.assertEqual(plant["name"], "John")
        self.assertEqual(plant["species"], "Rose")
        self.assertEqual(plant["watering_schedule"], "Twice a week")

    @patch("builtins.input", side_effect=["John", "Rose", "Twice a week"])
    def test_edit_plant(self, mock_input):
        db = self.test_db
        add_plant(db, "John", "Rose", "Twice a week")
        edit_plant(db, "John", {"species": "Tulip"})
        plant = db["plants"].find_one({"name": "John"})
        self.assertIsNotNone(plant)
        self.assertEqual(plant["name"], "John")
        self.assertEqual(plant["species"], "Tulip")
        self.assertEqual(plant["watering_schedule"], "Twice a week")

    @patch("builtins.input", side_effect=["John"])
    def test_delete_plant(self, mock_input):
        db = self.test_db
        add_plant(db, "John", "Rose", "Twice a week")
        delete_plant(db, "John")
        plant = db["plants"].find_one({"name": "John"})
        self.assertIsNone(plant)

    @patch("builtins.input", side_effect=["John"])
    def test_water_plant(self, mock_input):
        db = self.test_db
        add_plant(db, "John", "Rose", "Twice a week")
        water_plant(db, "John")
        plant = db["plants"].find_one({"name": "John"})
        self.assertIsNotNone(plant)
        self.assertIsNotNone(plant["last_watered"])

    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()
