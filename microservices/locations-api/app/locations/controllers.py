from datetime import datetime

from app.locations.models import Model as Location
from app.locations.schemas import LocationSchema as Schema
from app.locations.services import LocationService as Service
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("Locations", description="Locations API.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
class LocationsResource(Resource):
    @responds(schema=Schema, many=True)
    def get(self) -> List[Location]:
        locations: List[Location] = Service.retrieve_all()
        return locations


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
# TODO - handle not found
class LocationResource(Resource):
    @accepts(schema=Schema)
    @responds(schema=Schema)
    def post(self) -> Location:
        request.get_json()
        location: Location = Service.create(request.get_json())
        return location

    @responds(schema=Schema)
    def get(self, location_id) -> Location:
        location: Location = Service.retrieve(location_id)
        return location
