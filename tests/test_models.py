"""Sanity checks that the model taxonomy loads and migrations apply."""

from django.apps import apps
from django.contrib.gis.db import models as gis_models
from django.db import connection
from django.test import TestCase

from osmflex import models as osmflex_models


class ModelTaxonomyTests(TestCase):
    def test_expected_concrete_models_registered(self):
        registered = {m.__name__ for m in apps.get_app_config("osmflex").get_models()}
        expected = {
            "AmenityPoint",
            "AmenityLine",
            "AmenityPolygon",
            "BuildingPoint",
            "BuildingPolygon",
            "IndoorPoint",
            "IndoorLine",
            "IndoorPolygon",
            "InfrastructurePoint",
            "InfrastructureLine",
            "InfrastructurePolygon",
            "LandusePoint",
            "LandusePolygon",
            "LeisurePoint",
            "LeisurePolygon",
            "NaturalPoint",
            "NaturalLine",
            "NaturalPolygon",
            "PlacePoint",
            "PlaceLine",
            "PlacePolygon",
            "PoiPoint",
            "PoiLine",
            "PoiPolygon",
            "PublicTransportPoint",
            "PublicTransportLine",
            "PublicTransportPolygon",
            "RoadPoint",
            "RoadLine",
            "RoadPolygon",
            "RoadMajor",
            "ShopPoint",
            "ShopPolygon",
            "TrafficPoint",
            "TrafficLine",
            "TrafficPolygon",
            "WaterPoint",
            "WaterLine",
            "WaterPolygon",
            "Tags",
            "Unitable",
        }
        missing = expected - registered
        self.assertFalse(missing, f"Missing models: {missing}")

    def test_abstract_bases_are_abstract(self):
        for base in (osmflex_models.Osm, osmflex_models.OsmPoint, osmflex_models.OsmLine, osmflex_models.OsmPolygon):
            self.assertTrue(base._meta.abstract, f"{base.__name__} must be abstract")

    def test_point_geom_is_srid_3857(self):
        field = osmflex_models.RoadPoint._meta.get_field("geom")
        self.assertIsInstance(field, gis_models.PointField)
        self.assertEqual(field.srid, 3857)

    def test_line_geom_is_srid_3857(self):
        field = osmflex_models.RoadLine._meta.get_field("geom")
        self.assertIsInstance(field, gis_models.LineStringField)
        self.assertEqual(field.srid, 3857)

    def test_polygon_geom_is_srid_3857(self):
        field = osmflex_models.BuildingPolygon._meta.get_field("geom")
        self.assertIsInstance(field, gis_models.MultiPolygonField)
        self.assertEqual(field.srid, 3857)

    def test_tags_has_jsonb_column(self):
        field = osmflex_models.Tags._meta.get_field("tags")
        self.assertEqual(field.get_internal_type(), "JSONField")


class MigrationTests(TestCase):
    def test_road_line_table_exists(self):
        with connection.cursor() as c:
            c.execute(
                "SELECT 1 FROM information_schema.tables WHERE table_name = 'osmflex_roadline'",
            )
            self.assertIsNotNone(c.fetchone())

    def test_tags_table_exists(self):
        with connection.cursor() as c:
            c.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'osmflex_tags'")
            self.assertIsNotNone(c.fetchone())
