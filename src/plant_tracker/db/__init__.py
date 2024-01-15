from abc import ABC, abstractmethod


# Abstract class for database access
class Database(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_plant(self, name, species, watering_schedule):
        pass

    @abstractmethod
    def edit_plant(self, name, updates):
        pass

    @abstractmethod
    def delete_plant(self, name):
        pass

    @abstractmethod
    def water_plant(self, name):
        pass

    @abstractmethod
    def get_plants(self):
        pass
