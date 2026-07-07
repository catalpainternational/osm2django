from django.db import connection
from django.test import TestCase

from osmflex.models import RoadLine, Tags
from osmflex.utils import truncate_sql


def render(model) -> str:
    with connection.cursor() as c:
        return truncate_sql(model).as_string(c.cursor)


class TruncateSqlTests(TestCase):
    def test_road_line(self):
        self.assertEqual(render(RoadLine).strip(), 'TRUNCATE "osmflex_roadline" CASCADE;')

    def test_tags(self):
        self.assertEqual(render(Tags).strip(), 'TRUNCATE "osmflex_tags" CASCADE;')
