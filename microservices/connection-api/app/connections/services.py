import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app.connections.models import Connection, Location, Person
from app.connections.schemas import ConnectionSchema, PersonSchema
from app.connections.clients import LocationsApi, PersonsApi

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("connections-api")



class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[ConnectionSchema]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations = LocationsApi.retrieve_by_person(person_id, start_date, end_date)
        # TODO - handle error
        persons = PersonsApi.retrieve_all()
        # TODO - handle error
        person_map: Dict[str, Person] = {str(person.get("id", "-1")): person for person in persons}
        # TODO - retrieve locations per person instead of every person
        result: List[Connection] = []
        for location in locations:
            line = {
                    "person_id": person_id,
                    "longitude": location.get("longitude", "0"),
                    "latitude": location.get("latitude", "0"),
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            }
            locations = LocationsApi.calculate_location(line)
            # TODO - handle error
            for location in locations:
                logger.warning(f"location: {locations}")
                logger.warning(f"map: {person_map}")
                result.append(
                    Connection(
                        person=person_map[str(location["person_id"])], location=location,
                    )
                )

        return result

