from django.db import models
from neomodel import StructuredNode,StructuredRel, StringProperty, FloatProperty,IntegerProperty,UniqueIdProperty, RelationshipTo, Property, ZeroOrOne
from shapely.geometry import Point, Polygon


# Create your models here.

class TravelRel(StructuredRel):
    duration = IntegerProperty(required=True)
    departure_time = StringProperty(required=True)
    arrival_time = StringProperty(required=True)


class Station(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)
    destinations = RelationshipTo('Station','TRAVEL_TO', model=TravelRel)
    city=RelationshipTo('Area','HAS_TRAIN_STATION',model=StructuredRel, cardinality=ZeroOrOne)

class Area(StructuredNode):
    name = StringProperty(required=True)
    isin = RelationshipTo('Area','IS_IN')

class Communes(Area):
    stations=RelationshipTo('Station','HAS_TRAIN_STATION',model=StructuredRel)