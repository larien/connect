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