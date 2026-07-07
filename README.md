[![CI](https://github.com/catalpainternational/osm2django/actions/workflows/ci.yml/badge.svg)](https://github.com/catalpainternational/osm2django/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/osmflex.svg)](https://pypi.org/project/osmflex/)

# osmflex

A Django app that mirrors [pgosm-flex](https://github.com/rustprooflabs/pgosm-flex)
output, giving you an ORM-shaped view of OpenStreetMap data imported via
[osm2pgsql](https://osm2pgsql.org/).

## Stack

- Python 3.11+
- Django 5.2 LTS
- PostGIS 16-3.4+
- Package managed with [uv](https://github.com/astral-sh/uv)

## Install

```bash
uv add osmflex
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "django.contrib.gis",
    "osmflex",
]
```

## Import OSM data

`osmflex` ships two management commands:

```bash
./manage.py run_osm2pgsql /path/to/foo.osm.pbf   # writes schema osm.*
./manage.py import_from_pgosmflex --truncate     # upserts into osmflex_*
```

Then query with the Django ORM:

```python
>>> from osmflex.models import AmenityPoint
>>> AmenityPoint.objects.count()
14827
>>> AmenityPoint.objects.tagged()[:5]  # annotates each row with the full OSM tag JSONB
```

**End-to-end runnable example**: [`examples/minimal_import/`](./examples/minimal_import/)
walks through fetching a Geofabrik extract and running the full pipeline in a
disposable PostGIS container. Try:

```bash
cd examples/minimal_import
make db-up install migrate pbf import psql
```

## Docs

- [`docs/architecture.md`](./docs/architecture.md) — the pgosm-flex → Django
  pipeline, taxonomy, SRID choice, how `upsert_sql` mangles source-table names,
  how to add your own `Osm` subclass.
- [`docs/api.md`](./docs/api.md) — cheatsheet of every public export.

## Prerequisites

- **`osm2pgsql` ≥ 1.6** — install via package manager (`sudo apt install
  osm2pgsql` on modern Ubuntu; `brew install osm2pgsql` on macOS) or
  [build from source](https://osm2pgsql.org/doc/manual.html#installing).
- **PostGIS** — 3.4+ recommended.
- The bundled pgosm-flex LUA config in `osmflex/management/flex-config/` is
  sourced from [rustprooflabs/pgosm-flex](https://github.com/rustprooflabs/pgosm-flex).

## Development

```bash
uv sync --dev
uv run pytest              # 24 tests
uv run ruff check .
uv run mypy osmflex
```

## Releasing

Releases are automated via `.github/workflows/release.yml` using PyPI Trusted
Publishing (OIDC). To cut a release:

1. Bump `version` in `pyproject.toml` on `main`; merge.
2. Tag the merged commit with the same version (no `v` prefix):
   ```bash
   git tag 0.3.1 && git push origin 0.3.1
   ```
3. The workflow verifies tag/pyproject match, builds sdist + wheel, publishes to
   PyPI, and creates a GitHub Release with generated notes.
