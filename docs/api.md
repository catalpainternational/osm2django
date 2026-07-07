# API cheatsheet

Everything exported from `osmflex.*` at a glance. For architecture, see
[architecture.md](./architecture.md). For a runnable example, see
[../examples/minimal_import/](../examples/minimal_import/).

## Top-level (`osmflex`)

Model classes are **not** re-exported at package level (that would trip
Django's app-registry check on import). Import them from `osmflex.models`.

```python
from osmflex import truncate_sql, upsert_sql
```

| Name           | Kind      | Purpose                                                                     |
| -------------- | --------- | --------------------------------------------------------------------------- |
| `truncate_sql` | function  | Render `TRUNCATE {table} CASCADE` for a Django model class.                 |
| `upsert_sql`   | function  | Render `INSERT ... ON CONFLICT DO UPDATE` from the parallel `osm.*` source. |

## `osmflex.models`

### Roots

| Name         | Kind     | Notes                                                            |
| ------------ | -------- | ---------------------------------------------------------------- |
| `Osm`        | abstract | PK `osm_id`, columns `osm_type`, `name`. Uses `OsmTagged` manager. |
| `OsmPoint`   | abstract | Adds `geom: PointField(srid=3857)` + GiST index.                 |
| `OsmLine`    | abstract | Adds `geom: LineStringField(srid=3857)` + GiST index.            |
| `OsmPolygon` | abstract | Adds `geom: MultiPolygonField(srid=3857)` + GiST index.          |
| `OsmTagged`  | manager  | `.tagged()` annotates each row with the `tags` JSONB.            |

### Category mixins (all abstract)

`Amenity`, `Building`, `Indoor`, `Infrastructure`, `Landuse`, `Leisure`,
`Natural`, `Place`, `Poi`, `PublicTransport`, `Road`, `Shop`, `Traffic`,
`Water`, `WheelchairAccess` — see the per-class docstrings in
[`osmflex/models.py`](../osmflex/models.py) for what OSM tag set each captures.

### Concrete tables

Named `<Category><Geometry>` — see [architecture.md](./architecture.md) for
the full grid. Examples: `RoadLine`, `AmenityPoint`, `BuildingPolygon`,
`PublicTransportLine`, `RoadMajor`.

### Sidecars

| Name       | Kind     | Notes                                                                   |
| ---------- | -------- | ----------------------------------------------------------------------- |
| `Tags`     | concrete | Full tag JSONB keyed by `osm_id`. Join via `OsmTagged.tagged()`.        |
| `Unitable` | concrete | Mixed-geometry debugging table; **not for production**.                 |

## `osmflex.utils`

```python
from osmflex.utils import truncate_sql, upsert_sql
```

- `truncate_sql(model: type[Model]) → sql.Composed` — `TRUNCATE ... CASCADE`.
- `upsert_sql(model: type[Model], exclude_fields: list[str] | None = None) → sql.Composed`
  — the workhorse UPSERT. `exclude_fields` drops columns from both the INSERT
  column list and the `DO UPDATE SET` clause.

Both return `psycopg2.sql.Composed`; execute via
`connection.cursor().execute(query)` or render for logs with
`query.as_string(cursor.cursor)`.

## Management commands

- `./manage.py run_osm2pgsql <pbf>` — wraps `osm2pgsql` with the pgosm-flex
  LUA config and writes to schema `osm.*`.
- `./manage.py import_from_pgosmflex [--truncate] [--unitable]` — walks every
  concrete `Osm` subclass, renders `upsert_sql(cls)`, and executes them under
  one transaction. With `--truncate` also emits a `TRUNCATE` per table first.
  `--unitable` includes the `Unitable` debug table.
