from ast import operator
from unicodedata import name
from django.contrib.gis.db import models

# Create your models here.

class Osm(models.Model):

    osm_id = models.BigIntegerField(null=True, blank=True)
    osm_type = models.CharField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)
    name = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class OsmPoint(Osm):
    geom = models.PointField(srid=3857)
    class Meta:
        abstract = True

class OsmLine(Osm):
    geom = models.LineStringField(srid=3857)
    class Meta:
        abstract = True

class OsmPolygon(Osm):
    geom = models.MultiPolygonField(srid=3857)
    class Meta:
        abstract = True


class Amenity(models.Model):

    housenumber = models.CharField(max_length=128, null=True, blank=True)
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    postcode = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        abstract = True

class WheelchairAccess(models.Model):
    wheelchair = models.CharField(max_length=128, null=True, blank=True)
    wheelchair_desc = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        abstract = True

class AmenityPoint(OsmPoint, Amenity, WheelchairAccess):
    pass

class AmenityLine(OsmLine, Amenity, WheelchairAccess):
    pass

class AmenityPolygon(OsmPolygon, Amenity, WheelchairAccess):
    pass

class Building(Amenity):
    """
    Building inherits from Amenity
    as it shares address + wheelchair stats
    """
    levels = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    operator = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class BuildingPoint(OsmPoint, Building, WheelchairAccess):
    pass

class BuildingPolygon(OsmPoint, Building, WheelchairAccess):
    pass

class Indoor(models.Model):
    layer = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    layer = models.TextField(null=True, blank=True)
    level = models.TextField(null=True, blank=True)
    room = models.TextField(null=True, blank=True)
    entrance = models.TextField(null=True, blank=True)
    door = models.TextField(null=True, blank=True)
    capacity = models.TextField(null=True, blank=True)
    highway = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

class IndoorPoint(OsmPoint, Indoor):
    pass

class IndoorPolygon(OsmPolygon, Indoor):
    pass

class IndoorLine(OsmLine, Indoor):
    pass


class Infrastucture(models.Model):

    ele = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    operator = models.CharField(max_length=1024, null=True, blank=True)
    material = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class InfrastucturePoint(OsmPoint, Infrastucture):
    pass


class InfrastuctureLine(OsmLine, Infrastucture):
    pass


class InfrastucturePolygon(OsmPolygon, Infrastucture):
    pass


class Landuse(models.Model):

    class Meta:
        abstract = True

class LandusePoint(OsmPoint, Landuse):
    pass


class LandusePolygon(OsmPolygon, Landuse):
    pass

class Leisure(models.Model):

    class Meta:
        abstract = True

class LeisurePoint(OsmPoint, Leisure):
    pass

class LeisurePolygon(OsmPolygon, Leisure):
    pass


class Natural(models.Model):

    ele = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class NaturalPoint(OsmPoint, Natural):
    pass


class NaturalLine(OsmLine, Natural):
    pass


class NaturalPolygon(OsmPolygon, Natural):
    pass

class Place(models.Model):

    boundary = models.CharField(max_length=1024, null=True, blank=True)
    admin_level = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class PlacePoint(OsmPoint, Place):
    pass

class PlaceLine(OsmLine, Place):
    pass

class PlacePolygon(OsmPolygon, Place):
    member_ids = models.JSONField()

class Poi(Amenity):
    class Meta:
        abstract = True

class PoiPoint(OsmPoint, Poi):
    pass

class PoiLine(OsmLine, Poi):
    pass

class PoiPolygon(OsmPolygon, Poi):
    pass

class PublicTransport(WheelchairAccess):

    public_transport = models.TextField(max_length=1024, null=True, blank=True)
    layer = models.IntegerField(null=True, blank=True)
    name = models.TextField(max_length=1024, null=True, blank=True)
    ref = models.TextField(max_length=1024, null=True, blank=True)
    operator = models.TextField(max_length=1024, null=True, blank=True)
    network = models.TextField(max_length=1024, null=True, blank=True)
    surface = models.TextField(max_length=1024, null=True, blank=True)
    bus = models.TextField(max_length=1024, null=True, blank=True)
    shelter = models.TextField(max_length=1024, null=True, blank=True)
    bench = models.TextField(max_length=1024, null=True, blank=True)
    lit = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class PublicTransportPoint(OsmPoint, PublicTransport):
    pass

class PublicTransportLine(OsmLine, PublicTransport):
    pass

class PublicTransportPolygon(OsmPolygon, PublicTransport):
    pass

class Road(models.Model):
    ref = models.CharField(max_length=1024, null=True, blank=True)
    maxspeed = models.IntegerField(null=True, blank=True)
    oneway = models.IntegerField(null=True, blank=True)
    layer = models.CharField(max_length=1024, null=True, blank=True)
    tunnel = models.CharField(max_length=1024, null=True, blank=True)
    bridge = models.CharField(max_length=1024, null=True, blank=True)
    access = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class RoadPoint(OsmPoint, Road):
    pass

class RoadLine(OsmLine, Road):
    pass

class RoadPolygon(OsmPolygon, Road):
    pass

class Shop(Amenity, WheelchairAccess):

    operator = models.CharField(max_length=1024, null=True, blank=True)
    brand = models.CharField(max_length=1024, null=True, blank=True)
    website = models.CharField(max_length=1024, null=True, blank=True)
    phone = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class ShopPoint(OsmPoint, Shop):
    pass

class ShopPolygon(OsmPolygon, Shop):
    pass

class Traffic(models.Model):

    class Meta:
        abstract = True

class TrafficPoint(OsmPoint, Traffic):
    pass

class TrafficLine(OsmLine, Traffic):
    pass

class TrafficPolygon(OsmPolygon, Traffic):
    pass


class UnitTable(models.Model):

    """
    Single table that can take any OSM object and any geometry.

    Notes from the LUA file:
    -- Converted from https://github.com/openstreetmap/osm2pgsql/blob/master/flex-config/unitable.lua
    --   to use JSONB instead of HSTORE and osm schema.
    --
    -------------------------
    --  WARNING:   This layer is NOT intended for production use!
    --  Use this to explore data when building proper structures!
    -------------------------
    --
    -- Includes tags in JSONB (does not rely on all_tags.lua)
    -- Does NOT include deep copy for easy use with "require" like other scripts in this project.

    """

    osm_id = models.BigIntegerField()
    geom_type = models.CharField(max_length=5, null=True, blank=True)  # N(ode), W(way), R(relation)
    tags = models.JSONField()
    geom = models.GeometryField(srid=3857)

class Water(models.Model):

    layer = models.IntegerField()
    tunnel = models.CharField(max_length=1024, null=True, blank=True)
    bridge = models.CharField(max_length=1024, null=True, blank=True)
    boat = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class WaterPoint(OsmPoint, Water):
    pass

class WaterLine(OsmLine, Water):
    pass

class WaterPolygon(OsmPolygon, Water):
    pass
