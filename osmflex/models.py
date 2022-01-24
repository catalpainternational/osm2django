import dataclasses
from typing import Iterable, Optional, Union, List
from django.contrib.gis.db import models
from django.contrib.gis.geos import WKBReader
from .helpers import (
    MajorRoadField,
    OsmIdField,
    OsmLineStringField,
    OsmMultiPolygonField,
    OsmNameField,
    OsmPointField,
    OsmSpeedField,
    OsmSubtypeField,
    OsmTagIntField,
    OsmTypeField,
    RouteCycleField,
    RouteFootField,
    RouteMotorField,
)
import osmium

wkbfab = osmium.geom.WKBFactory()
wkbreader = WKBReader()
from .helpers import OsmObject, OsmTagCharField


def get_model(nwr: OsmObject) -> List["Osm"]:
    """
    From an OSM object, determine the appropriate models to
    import data to
    """

    _amenity_types = ("amenity", "bench", "brewery")

    _poi_types = ("building", "shop", "amenity", "leisure", "man_made", "tourism", "landuse", "natural", "historic")

    _building_types = {"building", "building:part", "office", "door", "entrance"}

    _place_types = ("place", "boundary", "admin_level")

    _road_types = ("highway",)

    _indoor = ("indoor", "door", "entrance")

    _infra = ("aeroway", "amenity", "emergency", "highway", "man_made", "power", "utility")

    tags = nwr.tags

    if len(tags) == 1 and "created_by" in tags:
        return []

    if len(tags) == 1 and "source" in tags:
        return []

    models = []

    if isinstance(nwr, osmium.osm.Node):
        if any((tag in tags for tag in _amenity_types)):
            models.append(AmenityPoint)
        if any((tag in tags for tag in _place_types)):
            models.append(PlacePoint)
        if any((tag in tags for tag in _building_types)):
            models.append(BuildingPoint)
        if any((tag in tags for tag in _poi_types)):
            models.append(PoiPoint)
        if any((tag in tags for tag in _road_types)):
            models.append(RoadPoint)
        if any((tag in tags for tag in _indoor)):
            models.append(IndoorPoint)
        if any((tag in tags for tag in _infra)):
            models.append(InfrastructurePoint)
        if "shop" in tags:
            models.append(ShopPoint)

    if isinstance(nwr, osmium.osm.Way):
        if any((tag in tags for tag in _amenity_types)):
            models.append(AmenityLine)
        if any((tag in tags for tag in _place_types)):
            models.append(PlaceLine)
        if any((tag in tags for tag in _poi_types)):
            models.append(PoiLine)
        if any((tag in tags for tag in _road_types)):
            models.append(RoadLine)
        if any((tag in tags for tag in _indoor)):
            models.append(IndoorLine)
        if any((tag in tags for tag in _infra)):
            models.append(InfrastructureLine)

    if isinstance(nwr, osmium.osm.Area):
        if any((tag in tags for tag in _amenity_types)):
            models.append(AmenityPolygon)
        if any((tag in tags for tag in _place_types)):
            models.append(PlacePolygon)
        if any((tag in tags for tag in _building_types)):
            models.append(BuildingPolygon)
        if any((tag in tags for tag in _poi_types)):
            models.append(PoiPolygon)
        if any((tag in tags for tag in _road_types)):
            models.append(RoadPolygon)
        if any((tag in tags for tag in _indoor)):
            models.append(IndoorPolygon)
        if any((tag in tags for tag in _infra)):
            models.append(InfrastructurePolygon)
        if "shop" in tags:
            models.append(ShopPolygon)

    return models


class OsmTagged(models.Manager):
    def tagged(self):
        """
        Returns objects with their "tags" column appended
        """
        tags = Tags.objects.filter(osm_id=models.OuterRef("osm_id"))
        return self.get_queryset().annotate(tags=models.Subquery(tags.values("tags")))


class PgosmFlex(models.Model):
    imported = models.DateTimeField()
    osm_date = models.DateField()
    default_date = models.BooleanField()
    region = models.TextField()
    pgosm_flex_version = models.TextField()
    srid = models.TextField()
    project_url = models.TextField()
    osm2pgsql_version = models.TextField()
    language = models.TextField()
    osm2pgsql_mode = models.TextField()

    class Meta:
        managed = False
        db_table = "osmflex_pgosm_flex"


class Osm(models.Model):

    osm_id = OsmIdField(primary_key=True)
    osm_type = OsmTypeField(max_length=1024, null=True, blank=True)
    name = OsmNameField()

    objects = OsmTagged()

    def __str__(self):
        return f"{self.name or getattr(self, 'osm_subtype', None) or self.osm_type}({self.osm_id})"

    class Meta:
        abstract = True


class OsmPoint(Osm):
    geom = OsmPointField()

    class Meta:
        abstract = True


class OsmLine(Osm):
    geom = OsmLineStringField()

    class Meta:
        abstract = True


class OsmPolygon(Osm):
    geom = OsmMultiPolygonField()

    class Meta:
        abstract = True


class Amenity(models.Model):

    housenumber = OsmTagCharField(tag="addr:housenumber")
    street = OsmTagCharField(tag="addr:street")
    city = OsmTagCharField(tag="addr:city")
    state = OsmTagCharField(tag="addr:state")
    postcode = OsmTagCharField(tag="addr:postcode")

    address = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        address = f"{self.housenumber} {self.street}".strip()
        for add_part in ["city", "state", "postcode"]:
            add_text = getattr(self, add_part)
            if not address:
                address = add_text
            elif add_text:
                address = f"{address}, {add_text}"
        self.address = address
        super().save(*args, **kwargs)


class WheelchairAccess(models.Model):
    wheelchair = OsmTagCharField(tag="wheelchair")
    wheelchair_desc = OsmTagCharField(tag="wheelchair_desc")

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
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class BuildingPoint(OsmPoint, Building, WheelchairAccess):
    pass


class BuildingPolygon(OsmPolygon, Building, WheelchairAccess):
    pass


class Indoor(models.Model):
    layer = OsmTagIntField(tag="layer")
    level = OsmTagIntField(tag="level")
    room = OsmTagCharField(tag="room")
    entrance = OsmTagCharField(tag="entrance")
    door = OsmTagCharField(tag="door")
    capacity = OsmTagCharField(tag="capacity")
    highway = OsmTagCharField(tag="highway")

    class Meta:
        abstract = True

class IndoorPoint(OsmPoint, Indoor):
    pass


class IndoorPolygon(OsmPolygon, Indoor):
    pass


class IndoorLine(OsmLine, Indoor):
    pass


class Infrastructure(models.Model):

    ele = OsmTagCharField(tag="ele")
    height = OsmTagCharField(tag="height")
    operator = OsmTagCharField(tag="operator")
    material = OsmTagCharField(tag="material")
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

class InfrastructurePoint(OsmPoint, Infrastructure):
    pass


class InfrastructureLine(OsmLine, Infrastructure):
    pass


class InfrastructurePolygon(OsmPolygon, Infrastructure):
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

    ele = OsmTagCharField("ele")

    class Meta:
        abstract = True

class NaturalPoint(OsmPoint, Natural):
    pass


class NaturalLine(OsmLine, Natural):
    pass


class NaturalPolygon(OsmPolygon, Natural):
    pass


class Place(models.Model):

    boundary = OsmTagCharField("boundary")
    admin_level = OsmTagIntField("admin_level")

    class Meta:
        abstract = True

class PlacePoint(OsmPoint, Place):
    pass


class PlaceLine(OsmLine, Place):
    pass


class PlacePolygon(OsmPolygon, Place):
    member_ids = models.JSONField(null=True, blank=True)


class Poi(Amenity):
    operator = OsmTagCharField(tag="operator")
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class PoiPoint(OsmPoint, Poi):
    pass


class PoiLine(OsmLine, Poi):
    pass


class PoiPolygon(OsmPolygon, Poi):
    member_ids = models.JSONField(null=True, blank=True)
    pass


class PublicTransport(WheelchairAccess):

    public_transport = OsmTagCharField(tag="public_transport")
    layer = OsmTagCharField(tag="layer")
    name = OsmNameField()
    ref = OsmTagCharField(tag="ref")
    operator = OsmTagCharField(tag="operator")
    network = OsmTagCharField(tag="network")
    surface = OsmTagCharField(tag="surface")
    bus = OsmTagCharField(tag="bus")
    shelter = OsmTagCharField(tag="shelter")
    bench = OsmTagCharField(tag="bench")
    lit = OsmTagCharField(tag="lit")
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class PublicTransportPoint(OsmPoint, PublicTransport):
    pass


class PublicTransportLine(OsmLine, PublicTransport):
    pass


class PublicTransportPolygon(OsmPolygon, PublicTransport):
    pass


class Road(models.Model):
    ref = OsmTagCharField(tag="ref")
    maxspeed = OsmSpeedField(null=True, blank=True)
    layer = OsmTagCharField(tag="layer")
    tunnel = OsmTagCharField(tag="tunnel")
    bridge = OsmTagCharField(tag="bridge")
    access = OsmTagCharField(tag="access")

    class Meta:
        abstract = True


class RoadPoint(OsmPoint, Road):
    pass


class RoadLine(OsmLine, Road):
    oneway = OsmTagCharField(tag="oneway")
    major = MajorRoadField(null=True, default=False)
    route_foot = RouteFootField(null=True, default=False)
    route_cycle = RouteCycleField(null=True, default=False)
    route_motor = RouteMotorField(null=True, default=False)

class RoadPolygon(OsmPolygon, Road):
    major = MajorRoadField(null=True, default=False)
    route_foot = RouteFootField(null=True, default=False)
    route_cycle = RouteCycleField(null=True, default=False)
    route_motor = RouteMotorField(null=True, default=False)


class RoadMajor(OsmLine, Road):
    pass


class Shop(Amenity, WheelchairAccess):

    operator = OsmTagCharField(tag="operator")
    brand = OsmTagCharField(tag="brand")
    website = OsmTagCharField(tag="website")
    phone = OsmTagCharField(tag="phone")
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class ShopPoint(OsmPoint, Shop):
    pass


class ShopPolygon(OsmPolygon, Shop):
    pass


class Traffic(models.Model):
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class TrafficPoint(OsmPoint, Traffic):
    name = None
    pass


class TrafficLine(OsmLine, Traffic):
    name = None
    pass


class TrafficPolygon(OsmPolygon, Traffic):
    name = None
    pass


class Unitable(models.Model):

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

    # ALTER TABLE osmflex_unitable ADD COLUMN id bigint GENERATED BY DEFAULT AS IDENTITY;
    id = models.BigIntegerField(primary_key=True)
    osm_id = models.BigIntegerField()
    geom_type = models.CharField(max_length=5, null=True, blank=True)  # N(ode), W(way), R(relation)
    tags = models.JSONField()
    geom = models.GeometryField(srid=3857)

    def __str__(self):
        return f"{self.osm_id}" + " " + ",".join([f"{k}={v}" for k, v in self.tags.items()])


class Water(models.Model):

    layer = OsmTagIntField(tag="layer")
    tunnel = OsmTagCharField(tag="tunnel")
    bridge = OsmTagCharField(tag="bridge")
    boat = OsmTagCharField(tag="boat")
    osm_subtype = OsmSubtypeField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class WaterPoint(OsmPoint, Water):
    pass


class WaterLine(OsmLine, Water):
    pass


class WaterPolygon(OsmPolygon, Water):
    pass


class Tags(models.Model):
    geom_type = models.CharField(max_length=2, null=True, blank=True)
    osm_id = models.BigIntegerField(primary_key=True)
    tags = models.JSONField()

    def __str__(self):
        return f"{self.osm_id}" + " " + ",".join([f"{k}={v}" for k, v in self.tags.items()])
