from app.locations.models import Model as Location
from geoalchemy2.types import Geometry as GeometryType
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter


class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    start_date = fields.String(attribute="start_date")
    end_date = fields.String(attribute="end_date")
    meters = fields.Integer()
    creation_time = fields.DateTime()

    class Meta:
        model = Location