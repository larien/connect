import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.locations.models import Model as Location
from app.locations.schemas import LocationSchema as Schema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locations-api")


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
    def retrieve_all() -> List[Location]:
        return db.session.query(Location).all()

    @staticmethod
    def retrieve_all_by_person(person_id, start_date=0, end_date=0) -> List[Location]:
        return db.session.query(Location).filter(
            Location.person_id == person_id
        #).filter(Location.creation_time < end_date).filter(
        #    Location.creation_time >= start_date TODO - obtain start and end date from request
        ).all()

    @staticmethod
    def calculate_location(location: Dict) -> Location:
        validation_results: Dict = Schema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        logger.warning("payload: ", location)

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Location] = []

        for (
            exposed_person_id,
            location_id,
            exposed_lat,
            exposed_long,
            exposed_time,
        ) in db.engine.execute(query, **location):
            location = Location(
                id=location_id,
                person_id=exposed_person_id,
                creation_time=exposed_time,
            )
            location.set_wkt_with_coords(exposed_lat, exposed_long)
            result.append(location)

        return result


    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = Schema().validate(location)
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