"""Tests for `osmflex.utils.upsert_sql`.

Focus on the SQL structure and the source-table name mangling, not on execution
against a real database (that's covered by integration testing via the
management command).
"""

from django.db import connection
from django.test import TestCase

from osmflex.models import AmenityPoint, AmenityPolygon, PublicTransportPoint, RoadLine, RoadMajor
from osmflex.utils import upsert_sql


def render(model, **kwargs) -> str:
    """Render an upsert_sql call to a plain string via the current connection."""
    with connection.cursor() as c:
        return upsert_sql(model, **kwargs).as_string(c.cursor)


class UpsertSqlStructureTests(TestCase):
    def test_road_line_has_insert_and_conflict_clauses(self):
        rendered = render(RoadLine)
        self.assertIn('INSERT INTO "osmflex_roadline"', rendered)
        self.assertIn("ON CONFLICT", rendered)
        self.assertIn('ON CONSTRAINT "osmflex_roadline_pkey"', rendered)
        self.assertIn("DO UPDATE SET", rendered)
        self.assertIn('FROM "osm"."road_line"', rendered)

    def test_amenity_point_source_table(self):
        rendered = render(AmenityPoint)
        self.assertIn('FROM "osm"."amenity_point"', rendered)

    def test_amenity_polygon_source_table(self):
        rendered = render(AmenityPolygon)
        self.assertIn('FROM "osm"."amenity_polygon"', rendered)

    def test_public_transport_source_table_gets_underscore(self):
        """The `publictransport` → `public_transport` transform is a source-table quirk."""
        rendered = render(PublicTransportPoint)
        self.assertIn('FROM "osm"."public_transport_point"', rendered)

    def test_road_major_source_table_gets_underscore(self):
        rendered = render(RoadMajor)
        self.assertIn('FROM "osm"."road_major"', rendered)


class UpsertSqlExcludeFieldsTests(TestCase):
    def test_exclude_removes_field_from_insert_columns(self):
        rendered = render(RoadLine, exclude_fields=["name"])
        # The literal identifier `"name"` should not appear in the rendered SQL.
        self.assertNotIn('"name"', rendered)

    def test_exclude_missing_field_is_noop(self):
        # No error, and known fields are still present.
        rendered = render(RoadLine, exclude_fields=["not_a_real_column"])
        self.assertIn('"osm_id"', rendered)
