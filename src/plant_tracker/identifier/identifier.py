import os

import requests
from dotenv import load_dotenv


class APIClient:
    def __init__(self):
        load_dotenv()
        self.PERENUAL_KEY = os.environ.get("PERENUAL_KEY")

    def get(self, query: str):
        url = f"https://perenual.com/api/species-list?key={self.PERENUAL_KEY}&q={query}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        try:
            species = data["data"]
            print(species)
            return_species = []
            for s in species:
                return_species.append(
                    {
                        "ID": s["id"],
                        "Common Name": s["common_name"],
                        "Scientific Names": s["scientific_name"],
                    }
                )
            return return_species
        except KeyError:
            print("No species found")
            return None
