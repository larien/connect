from datetime import datetime

from app.persons.models import Model as Person
from app.persons.schemas import PersonSchema as Schema
from app.persons.services import PersonService as Service
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("Persons", description="Persons API.")  # noqa


# TODO: This needs better exception handling

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=Schema)
    @responds(schema=Schema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = Service.create(payload)
        return new_person

    @responds(schema=Schema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = Service.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=Schema)
    def get(self, person_id) -> Person:
        person: Person = Service.retrieve(person_id)
        return person