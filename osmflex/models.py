import logging

from django.contrib.gis.db import models
from django.contrib.postgres.indexes import GistIndex

logger = logging.getLogger(__name__)


class OsmTagged(models.Manager):
    """Manager that annotates each row with its OSM `tags` JSONB from the `Tags` table."""

    def tagged(self):
        """Return the queryset with a subquery-annotated `tags` JSONB column."""
        tags = Tags.objects.filter(osm_id=models.OuterRef("osm_id"))
        return self.get_queryset().annotate(tags=models.Subquery(tags.values("tags")))

    class Meta:
        managed = False
        db_table = "osmflex_pgosm_flex"


class Osm(models.Model):
    """Root abstract model for every OSM-derived table.

    Every concrete `osmflex_*` table has `osm_id` as its primary key (matching
    OpenStreetMap's element id), plus `osm_type` and `name` columns populated
    by the pgosm-flex export.
    """

    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=1024, null=True, blank=True)
    name = models.CharField(max_length=1024, null=True, blank=True)

    objects = OsmTagged()

    def __str__(self):
        return f"{self.name or getattr(self, 'osm_subtype', None) or self.osm_type}({self.osm_id})"

    class Meta:
        abstract = True


class OsmPoint(Osm):
    """Abstract base for point-geometry tables (SRID 3857, GiST-indexed)."""

    geom = models.PointField(srid=3857)

    class Meta:
        abstract = True
        indexes = [GistIndex(fields=["geom"])]


class OsmLine(Osm):
    """Abstract base for linestring-geometry tables (SRID 3857, GiST-indexed)."""

    geom = models.LineStringField(srid=3857)

    class Meta:
        abstract = True
        indexes = [GistIndex(fields=["geom"])]


class OsmPolygon(Osm):
    """Abstract base for multipolygon-geometry tables (SRID 3857, GiST-indexed)."""

    geom = models.MultiPolygonField(srid=3857)

    class Meta:
        abstract = True
        indexes = [GistIndex(fields=["geom"])]


class Amenity(models.Model):
    """OSM `amenity=*` tag family: postal address fields shared across amenity variants."""

    housenumber = models.CharField(max_length=512, null=True, blank=True)
    street = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=512, null=True, blank=True)
    state = models.CharField(max_length=512, null=True, blank=True)
    postcode = models.CharField(max_length=512, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True


class WheelchairAccess(models.Model):
    """OSM `wheelchair=*` accessibility tags. Mixed into amenity/POI/transport tables."""

    wheelchair = models.CharField(max_length=512, null=True, blank=True)
    wheelchair_desc = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True


class AmenityPoint(OsmPoint, Amenity, WheelchairAccess):
    pass


class AmenityLine(OsmLine, Amenity, WheelchairAccess):
    pass


class AmenityPolygon(OsmPolygon, Amenity, WheelchairAccess):
    pass


class Building(Amenity):
    """OSM `building=*`. Inherits address fields from `Amenity` and adds structural attributes (levels, height, operator)."""

    levels = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    operator = models.CharField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class BuildingPoint(OsmPoint, Building, WheelchairAccess):
    pass


class BuildingPolygon(OsmPolygon, Building, WheelchairAccess):
    pass


class Indoor(models.Model):
    """OSM `indoor=*` tag family: rooms, doors, corridors, level references."""

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


class Infrastructure(models.Model):
    """OSM `man_made=*` / tower / pipeline / power infrastructure (elevation, height, material, operator)."""

    ele = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    operator = models.CharField(max_length=1024, null=True, blank=True)
    material = models.CharField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class InfrastructurePoint(OsmPoint, Infrastructure):
    pass


class InfrastructureLine(OsmLine, Infrastructure):
    pass


class InfrastructurePolygon(OsmPolygon, Infrastructure):
    pass


class Landuse(models.Model):
    """OSM `landuse=*` (residential, industrial, farmland, etc.). No extra fields; the base `Osm` columns suffice."""

    class Meta:
        abstract = True


class LandusePoint(OsmPoint, Landuse):
    pass


class LandusePolygon(OsmPolygon, Landuse):
    pass


class Leisure(models.Model):
    """OSM `leisure=*` (parks, pitches, playgrounds). No extra fields; the base `Osm` columns suffice."""

    class Meta:
        abstract = True


class LeisurePoint(OsmPoint, Leisure):
    pass


class LeisurePolygon(OsmPolygon, Leisure):
    pass


class Natural(models.Model):
    """OSM `natural=*` (peaks, ridges, coastline features). Adds an elevation column."""

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
    """OSM `place=*` and administrative boundaries: `boundary`, `admin_level` for country/state/city hierarchies."""

    boundary = models.CharField(max_length=1024, null=True, blank=True)
    admin_level = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class PlacePoint(OsmPoint, Place):
    pass


class PlaceLine(OsmLine, Place):
    pass


class PlacePolygon(OsmPolygon, Place):
    member_ids = models.JSONField(null=True, blank=True)


class Poi(Amenity):
    """Points of interest: catch-all for tagged features not covered by more specific categories. Inherits address from `Amenity`."""

    operator = models.CharField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

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
    """OSM `public_transport=*`: bus stops, platforms, networks, shelters. Inherits wheelchair accessibility."""

    public_transport = models.TextField(max_length=1024, null=True, blank=True)
    layer = models.IntegerField(null=True, blank=True)
    ref = models.TextField(max_length=1024, null=True, blank=True)
    operator = models.TextField(max_length=1024, null=True, blank=True)
    network = models.TextField(max_length=1024, null=True, blank=True)
    surface = models.TextField(max_length=1024, null=True, blank=True)
    bus = models.TextField(max_length=1024, null=True, blank=True)
    shelter = models.TextField(max_length=1024, null=True, blank=True)
    bench = models.TextField(max_length=1024, null=True, blank=True)
    lit = models.TextField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class PublicTransportPoint(OsmPoint, PublicTransport):
    pass


class PublicTransportLine(OsmLine, PublicTransport):
    pass


class PublicTransportPolygon(OsmPolygon, PublicTransport):
    pass


class Road(models.Model):
    """OSM `highway=*` roads: reference number, speed limit, bridge/tunnel flags. Concrete subclasses add oneway/access/major flags."""

    ref = models.CharField(max_length=1024, null=True, blank=True)
    maxspeed = models.IntegerField(null=True, blank=True)
    layer = models.CharField(max_length=1024, null=True, blank=True)
    tunnel = models.CharField(max_length=1024, null=True, blank=True)
    bridge = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class RoadPoint(OsmPoint, Road):
    oneway = models.IntegerField(null=True, blank=True)
    access = models.CharField(max_length=1024, null=True, blank=True)


class RoadLine(OsmLine, Road):
    major = models.BooleanField(null=True, default=False)
    route_foot = models.BooleanField(null=True, default=False)
    route_cycle = models.BooleanField(null=True, default=False)
    route_motor = models.BooleanField(null=True, default=False)
    oneway = models.IntegerField(null=True, blank=True)
    access = models.CharField(max_length=1024, null=True, blank=True)


class RoadPolygon(OsmPolygon, Road):
    major = models.BooleanField(null=True, default=False)
    route_foot = models.BooleanField(null=True, default=False)
    route_cycle = models.BooleanField(null=True, default=False)
    route_motor = models.BooleanField(null=True, default=False)
    access = models.CharField(max_length=1024, null=True, blank=True)


class RoadMajor(OsmLine, Road):
    major = models.BooleanField(null=True, default=False)


class Shop(Amenity, WheelchairAccess):
    """OSM `shop=*`: commercial premises with brand, operator, contact details. Inherits address + wheelchair accessibility."""

    operator = models.CharField(max_length=1024, null=True, blank=True)
    brand = models.CharField(max_length=1024, null=True, blank=True)
    website = models.CharField(max_length=1024, null=True, blank=True)
    phone = models.CharField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class ShopPoint(OsmPoint, Shop):
    pass


class ShopPolygon(OsmPolygon, Shop):
    pass


class Traffic(models.Model):
    """OSM traffic signs, signals, calming devices. Concrete subclasses drop `name` because these features are unnamed."""

    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class TrafficPoint(OsmPoint, Traffic):
    name = None  # type: ignore


class TrafficLine(OsmLine, Traffic):
    name = None  # type: ignore


class TrafficPolygon(OsmPolygon, Traffic):
    name = None  # type: ignore


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

    osm_id = models.BigIntegerField()
    geom_type = models.CharField(max_length=5, null=True, blank=True)  # N(ode), W(way), R(relation)
    tags = models.JSONField()
    geom = models.GeometryField(srid=3857)

    def __str__(self):
        return f"{self.osm_id}" + " " + ",".join([f"{k}={v}" for k, v in self.tags.items()])


class Water(models.Model):
    """OSM `waterway=*` and water bodies: bridges, tunnels, navigability."""

    layer = models.IntegerField()
    tunnel = models.CharField(max_length=1024, null=True, blank=True)
    bridge = models.CharField(max_length=1024, null=True, blank=True)
    boat = models.CharField(max_length=1024, null=True, blank=True)
    osm_subtype = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True


class WaterPoint(OsmPoint, Water):
    pass


class WaterLine(OsmLine, Water):
    pass


class WaterPolygon(OsmPolygon, Water):
    pass


class Tags(models.Model):
    """Sidecar table holding the full OSM tag JSONB for every element.

    Concrete `osmflex_*` tables only store the columns of interest for each
    category; when you need arbitrary tags, join to `Tags` via `osm_id` — see
    `OsmTagged.tagged()` for the standard annotated-queryset accessor.
    """

    geom_type = models.CharField(max_length=2, null=True, blank=True)
    osm_id = models.BigIntegerField(primary_key=True)
    tags = models.JSONField()

    def __str__(self):
        return f"{self.osm_id}" + " " + ",".join([f"{k}={v}" for k, v in self.tags.items()])
