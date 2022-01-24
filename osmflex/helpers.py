# Port of pgosm-flex to python

from dataclasses import dataclass
from typing import Dict, Optional, Union
from dataclasses import dataclass
import warnings
from django.contrib.gis.db import models
from osmium import osm

from django.contrib.gis.geos import WKBReader
import osmium

wkbfab = osmium.geom.WKBFactory()
wkbreader = WKBReader()

OsmObject = Union[osm.Node, osm.Way, osm.Area]


def parse_to_meters(value: str) -> int:
    """
    Parse a tag value like "1800", "1955 m" or "8001 ft" and return a number in meters
    """
    if value.isnumeric():
        return float(value)
    elif value.endswith("m"):
        return float(value[:-1])
    elif value.endswith("ft"):
        return float(value[:-2]) * 0.3048
    else:
        return None


class OsmSpeedField(models.IntegerField):
    @classmethod
    def from_osm(cls, osmobject):
        try:
            value = osmobject.tags.get("maxspeed")
            if not value:
                return None

            if value.isnumeric():
                return float(value)

            if value.endswith("mph"):
                value = value[:-3] * 1.60934
                return value
        except Exception as E:
            warnings.warn(f"{E}")
            return None



class OsmTypeField(models.CharField):

    @staticmethod
    def from_osm(osmobject: OsmObject):
        """
        Return the OSM type of an object
        This is a semi arbitrary category based on tags
        """
        def address_only_building(tags_):

            not_address_only = ["shop", "amenity", "building", "building:part", "leisure", "landuse", "office", "tourism"]

            for tag in not_address_only:
                if tag in tags_:
                    return False

            for t in tags_:
                if t.k.startswith("addr:"):
                    return True

            return False

        tags = osmobject.tags
        # Amenity
        for k in ["amenity", "brewery", "bench"]:
            v = tags.get(k)
            if v:
                return v

        # Transport
        for k in ["bus", "railway", "lightrail", "train", "aerialway", "highway", "public_transport"]:
            v = tags.get(k)
            if v:
                return v

        # Point of Interest
        for k in ["shop", "amenity", "building", "leisure", "landuse", "natural", "man_made", "tourism", "historic"]:
            v = tags.get(k)
            # Because we subtype these return the key
            if v:
                return k

        # Infra.
        if tags.get("amenity") == "fire_hydrant" or tags.get("emergency") == "fire_hydrant":
            return "fire_hydrant"
        elif tags.get("amenity") == "emergency_phone" or tags.get("emergency") == "phone":
            return "emergency_phone"
        elif tags.get("highway") == "emergency_access_point":
            return "emergency_access"
        elif tags.get("man_made") in ("tower", "communications_tower", "mast", "lighthouse", "flagpole"):
            return tags.get("man_made")
        elif tags.get("man_made") in ("silo", "storage_tank", "water_tower", "reservoir_covered"):
            return tags.get("man_made")
        elif tags.get("power"):
            return "power"
        elif tags.get("utility"):
            return "utility"

        if "building" in tags:
            return "building"
        elif "building:part" in tags:
            return "building_part"
        elif "office" in tags:
            return "office"
        elif address_only_building(tags_ = tags):
            return "address"
        elif "entrance" in tags:
            return "entrance"
        elif "door" in tags:
            return "door"

        return "unknown"


class OsmSubtypeField(models.CharField):
    @staticmethod
    def from_osm(osmobject: OsmObject):
        tags = osmobject.tags
        # Point of Interest
        for k in ["shop", "amenity", "building", "leisure", "landuse", "natural", "man_made", "tourism", "historic"]:
            v = tags.get(k)
            # These are subtypes
            if v:
                return v

        return "unknown"


class RouteFootField(models.BooleanField):

    @staticmethod
    def from_osm(osmobject: OsmObject):
        tags = osmobject.tags
        access_false = ("no", "private")
        foot_false = ("no", "private")
        foot_true = ("yes", "permissive", "designated")
        highway_true = (
            "pedestrian",
            "crossing",
            "platform",
            "social_path",
            "steps",
            "trailhead",
            "track",
            "path",
            "unclassified",
            "service",
            "residential",
            "living_street",
            "elevator",
            "corridor",
            "foot",
        )

        if "footway" in tags:
            return True
        if tags.get("access") in access_false:
            return False
        if tags.get("foot") in foot_false:
            return False
        if tags.get("foot") in foot_true:
            return True
        if tags.get("highway") in highway_true:
            return True


class RouteCycleField(models.BooleanField):
    @staticmethod
    def from_osm(osmobject: OsmObject):
        tags = osmobject.tags
        access_false = ("no", "private")
        cycle_false = ("no", "private")
        cycle_true = ("yes", "permissive", "designated")
        highway_true = (
            "cycleway"
            "track"
            "path"
            "unclassified"
            "service"
            "residential"
            "tertiary"
            "tertiary_link"
            "secondary"
            "secondary_link"
            "living_street"
        )

        if "cycleway" in tags:
            return True
        if tags.get("access") in access_false:
            return False
        if tags.get("foot") in cycle_false:
            return False
        if tags.get("bicycle") in cycle_true:
            return True
        if tags.get("highway") in highway_true:
            return True


class RouteMotorField(models.BooleanField):
    @staticmethod
    def from_osm(osmobject: OsmObject):
        tags = osmobject.tags
        motor_vehicle_access_false = ("no", "private")
        highway_true = (
            "motorway",
            "motorway_link",
            "trunk",
            "trunk_link",
            "primary",
            "primary_link",
            "secondary",
            "secondary_link",
            "tertiary",
            "tertiary_link",
            "residential",
            "service",
            "unclassified",
            "living_street",
            "rest_area",
            "raceway",
        )

        if "cycleway" in tags:
            return True
        if tags.get("access") in motor_vehicle_access_false:
            return False
        if tags.get("highway") in highway_true:
            return True
        if tags.get("motor_vehicle") in ("yes", "permissive"):
            return True


class MajorRoadField(models.BooleanField):
    @staticmethod
    def from_osm(osmobject: OsmObject):
        return osmobject.tags.get("highway") in (
            "motorway",
            "motorway_link",
            "primary",
            "primary_link",
            "secondary",
            "secondary_link",
            "tertiary",
            "tertiary_link",
            "trunk",
            "trunk_link",
        )


class OsmTagCharField(models.CharField):
    def __init__(self, tag="", *args, **kwargs):
        self.tag = tag
        kwargs["max_length"] = kwargs.get("max_length", 1024)
        kwargs["null"] = kwargs.get("null", True)
        kwargs["blank"] = kwargs.get("blank", True)
        super().__init__(*args, **kwargs)

    def from_osm(self, osmobject: OsmObject):
        return osmobject.tags.get(self.tag)


class OsmTagIntField(models.IntegerField):

    def __init__(self, tag="", *args, **kwargs):
        self.tag = tag
        kwargs["null"] = kwargs.get("null", True)
        kwargs["blank"] = kwargs.get("blank", True)
        super().__init__(*args, **kwargs)


    def from_osm(self, osmobject: OsmObject):
        if self.tag not in osmobject.tags:
            return None
        try:
            return int(osmobject.tags.get(self.tag))
        except Exception as E:
            warnings.warn(f"{E}")


class OsmNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = kwargs.get("max_length", 1024)
        kwargs["null"] = kwargs.get("null", True)
        kwargs["blank"] = kwargs.get("blank", True)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_osm(osmobject: OsmObject):
        tags = osmobject.tags
        for tag in ["name", "short_name", "alt_name", "loc_name"]:
            if tag in tags:
                return tags[tag]
        """
        -- Uses tags.old_name first if exists.
        -- Looks for any name tag associated with a colon.
        -- Gives zero priority, simply the first found value.
        -- And empty string for real last ditch.
        """
        if "old_name" in tags:
            return tags.get("old_name")

        for tag in tags:
            if tag.k.startswith("name:") or tag.k.endswith(":NAME"):
                return tag.v


class OsmIdField(models.BigIntegerField):
    @staticmethod
    def from_osm(osmobject: OsmObject):
        return osmobject.id


class OsmPointField(models.PointField):
    def __init__(self, *args, **kwargs):
        kwargs["srid"] = kwargs.pop('srid', 3857)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_osm(osmobject:OsmObject):
        geom = wkbreader.read(wkbfab.create_point(osmobject).encode())
        geom.srid = 4326
        geom.transform(3857)
        return geom


class OsmLineStringField(models.LineStringField):
    def __init__(self, *args, **kwargs):
        kwargs["srid"] = kwargs.pop('srid', 3857)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_osm(osmobject:OsmObject):
        geom = wkbreader.read(wkbfab.create_linestring(osmobject).encode())
        geom.srid = 4326
        geom.transform(3857)
        return geom


class OsmMultiPolygonField(models.MultiPolygonField):
    def __init__(self, *args, **kwargs):
        kwargs["srid"] = kwargs.pop('srid', 3857)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_osm(osmobject:OsmObject):
        geom = wkbreader.read(wkbfab.create_multipolygon(osmobject).encode())
        geom.srid = 4326
        geom.transform(3857)
        return geom
