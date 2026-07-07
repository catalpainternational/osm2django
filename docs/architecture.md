# Architecture

`osmflex` is a thin Django app that mirrors the schema produced by
[**pgosm-flex**](https://github.com/rustprooflabs/pgosm-flex) — an
[osm2pgsql](https://osm2pgsql.org/) LUA output that writes a normalized,
category-first set of tables. This document explains the pipeline, the
taxonomy, and how to extend it.

## Pipeline

```
   Geofabrik .osm.pbf
           │
           │   ./manage.py run_osm2pgsql /path/to/foo.osm.pbf
           ▼
    schema  osm.*              (osm2pgsql writes here via pgosm-flex LUA)
    ├── osm.road_line
    ├── osm.amenity_point
    ├── osm.building_polygon
    └── osm.tags              (all OSM tags as JSONB)
           │
           │   ./manage.py import_from_pgosmflex [--truncate] [--unitable]
           ▼
    schema  public.osmflex_*   (Django-managed tables)
    ├── osmflex_roadline       ← INSERT ... ON CONFLICT DO UPDATE
    ├── osmflex_amenitypoint
    ├── osmflex_buildingpolygon
    └── osmflex_tags
```

The `import_from_pgosmflex` command walks every non-abstract subclass of
`osmflex.models.Osm`, renders an UPSERT statement via
`osmflex.utils.upsert_sql`, and executes them inside a single
`transaction.atomic()` block. The command is idempotent — re-running it
after a fresh `run_osm2pgsql` refreshes rows in place.

## Taxonomy: category × geometry

Concrete models are named `<Category><Geometry>`:

| Category            | `Point` | `Line` | `Polygon` | Extra                   |
| ------------------- | :-----: | :----: | :-------: | ----------------------- |
| `Amenity`           | ✅       | ✅      | ✅         |                         |
| `Building`          | ✅       |        | ✅         |                         |
| `Indoor`            | ✅       | ✅      | ✅         |                         |
| `Infrastructure`    | ✅       | ✅      | ✅         |                         |
| `Landuse`           | ✅       |        | ✅         |                         |
| `Leisure`           | ✅       |        | ✅         |                         |
| `Natural`           | ✅       | ✅      | ✅         |                         |
| `Place`             | ✅       | ✅      | ✅         |                         |
| `Poi`               | ✅       | ✅      | ✅         |                         |
| `PublicTransport`   | ✅       | ✅      | ✅         |                         |
| `Road`              | ✅       | ✅      | ✅         | plus `RoadMajor` (Line) |
| `Shop`              | ✅       |        | ✅         |                         |
| `Traffic`           | ✅       | ✅      | ✅         |                         |
| `Water`             | ✅       | ✅      | ✅         |                         |

Each concrete model inherits from:
1. **One geometry base** — `OsmPoint`, `OsmLine`, or `OsmPolygon`. Provides
   the `geom` field (SRID 3857, GiST-indexed) plus `osm_id`/`osm_type`/`name`
   from `Osm`.
2. **One category mixin** — `Amenity`, `Building`, `Road`, etc. Provides the
   category-specific columns (address for `Amenity`, `maxspeed` for `Road`,
   `wheelchair` for `PublicTransport`, …).

Two sidecar models don't fit the taxonomy:

- **`Tags`** — an `osm_id`-keyed JSONB dump of every OSM tag. Join to it via
  `OsmTagged.tagged()` when you need arbitrary key/value access beyond the
  columns that pgosm-flex materializes.
- **`Unitable`** — a mixed-geometry debugging table (not for production use).

## SRID choice

All geometries are stored in **EPSG:3857 (Web Mercator)** because:

- Vector tiles (`ST_AsMVT`) require 3857.
- pgosm-flex writes in 3857 by default.
- Reprojecting on read is more expensive than reprojecting once at import time.

If your downstream needs a different SRID, project on read or subclass a
geometry base with a different `srid=`.

## `upsert_sql`: source-table name mangling

`upsert_sql(RoadLine)` renders `INSERT INTO "osmflex_roadline" ... FROM
"osm"."road_line" ...`. The Django table name has no underscores because of
Django's default `<app>_<model>` scheme; the source table has them because
pgosm-flex uses snake_case. The mapping is deterministic string surgery in
[`osmflex/utils.py`](../osmflex/utils.py):

- strip `osmflex_` prefix
- replace `point` → `_point`, `line` → `_line`, `polygon` → `_polygon`
- special-case `publictransport` → `public_transport`
- special-case `roadmajor` → `road_major`

Adding a new category with a name that already contains internal underscores
(e.g. `Amenity` → `amenity`) works without a special case; new multi-word
categories will need one.

## Adding a custom `Osm` subclass

To add your own OSM-derived table:

1. Create a category mixin (abstract) with your extra columns.
2. Combine it with a geometry base:
   ```python
   from osmflex.models import OsmPoint

   class Volcano(models.Model):
       last_eruption_year = models.IntegerField(null=True)

       class Meta:
           abstract = True

   class VolcanoPoint(OsmPoint, Volcano):
       pass
   ```
3. `makemigrations` in your own app.
4. Add a corresponding source view to your pgosm-flex LUA config, e.g. a
   view `osm.volcano_point` selecting `natural=volcano` features. `osmflex`'s
   `import_from_pgosmflex` will automatically walk your subclass (via
   `get_all_subclasses(Osm)`) and generate the UPSERT.

The source-table name it will look for is derived from your model's
`db_table` per the rules above; either accept the default naming or set
`class Meta: db_table = "..."` explicitly.
