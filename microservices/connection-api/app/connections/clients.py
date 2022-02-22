import requests
import os
from app.connections.schemas import PersonSchema, LocationSchema
from typing import List

class PersonsApi:
    @staticmethod
    def retrieve_all() -> List[PersonSchema]:
        response = requests.get(os.getenv("PERSONS_API_RETRIEVE_ALL"), verify=False)
        if response.status_code != requests.codes.ok:
            return "failures"
        print("print: ", response)
        return response.json()

class LocationsApi:
    @staticmethod
    def retrieve_by_person(person_id, start_date, end_date) -> List[PersonSchema]:
        # TODO - query param (creation time, person id)
        response = requests.get(os.getenv("LOCATIONS_API")+"locations/person/"+person_id, verify=False)
        if response.status_code != requests.codes.ok:
            return "failures"
        print("print: ", response)
        return response.json()

    @staticmethod
    def calculate_location(location) -> List[LocationSchema]:
        
        response = requests.post(os.getenv("LOCATIONS_API")+"locations/calculate", json=location)
        if response.status_code != requests.codes.ok:
            return response.text
        return response.json()