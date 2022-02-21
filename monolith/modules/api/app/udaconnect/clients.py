import requests
import os
from app.udaconnect.models import Person
from typing import List

class PersonsApi:
    @staticmethod
    def retrieve_all() -> List[Person]:
        response = requests.get(os.getenv("PERSONS_API_RETRIEVE_ALL"), verify=False)
        if response.status_code != requests.codes.ok:
            return "failures"
        print("print: ", response)
        return response.json()

class LocationsApi:
    @staticmethod
    def retrieve_by_person(person_id, start_date, end_date) -> List[Person]:
        # TODO - query param (creation time, person id)
        response = requests.get(os.getenv("LOCATIONS_API")+"locations/person/"+person_id, verify=False)
        if response.status_code != requests.codes.ok:
            return "failures"
        print("print: ", response)
        return response.json()