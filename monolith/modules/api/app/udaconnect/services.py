import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.clients import PersonsApi, LocationsApi
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("connect-api")


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
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


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location