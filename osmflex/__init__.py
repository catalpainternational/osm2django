"""osmflex: Django app + management commands for the pgosm-flex OSM export.

Models live in :mod:`osmflex.models` and are not re-exported here because
importing them at package-import time would trip Django's app-registry check.

Import model classes as::

    from osmflex.models import Osm, OsmPoint, RoadLine

Utility SQL generators are safe to re-export::

    from osmflex import truncate_sql, upsert_sql

See ``docs/architecture.md`` for the pipeline and ``docs/api.md`` for the
full export list.
"""

from osmflex.utils import truncate_sql, upsert_sql

__all__ = ["truncate_sql", "upsert_sql"]
