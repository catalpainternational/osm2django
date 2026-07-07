# Minimal osmflex import — runbook

A small standalone Django project that installs `osmflex` from PyPI and
imports an `.osm.pbf` extract end-to-end. Not shipped in the `osmflex` wheel.

## Prerequisites

- Docker (for the PostGIS container)
- `osm2pgsql` ≥ 1.6 on your host (`sudo apt install osm2pgsql` on modern
  Ubuntu; check with `osm2pgsql --version`)
- Python ≥ 3.11 with `uv` installed (`pipx install uv` or
  `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A `.osm.pbf` extract. Small ones from Geofabrik work well:
  <https://download.geofabrik.de/> — e.g. Papua New Guinea (~55 MB).

## Quick start

```bash
make db-up            # start the PostGIS container on :49155
make install          # uv venv + install osmflex
make migrate          # apply migrations
make pbf              # download the default PBF (East Timor, ~5 MB) to ./pbf/
make import           # runs run_osm2pgsql then import_from_pgosmflex --truncate
make psql             # `select count(*) from osmflex_roadline;`
```

To use your own extract, drop it in `./pbf/` and either edit `PBF=` in the
`Makefile` or run `make import PBF=./pbf/your-file.osm.pbf`.

## Layout

```
examples/minimal_import/
├── Makefile              # one-line orchestration
├── docker-compose.yml    # postgis:16-3.4 on port 49155
├── manage.py             # standard Django entry
├── project/
│   ├── __init__.py
│   ├── settings.py       # bare Django + osmflex + gis, PostGIS config
│   └── urls.py           # empty admin-only URLconf
└── pyproject.toml        # osmflex dep, uv-managed
```

## Cleanup

```bash
make db-down          # stop and remove the PostGIS container + volume
```

## Notes

- The default DB volume is ephemeral. If you want persistence, comment
  out the `tmpfs:` line in `docker-compose.yml`.
- `run_osm2pgsql` requires `osm2pgsql` on the *host*, not in the container.
  It connects to the DB using the credentials in `project/settings.py`.
- `import_from_pgosmflex --truncate` empties the destination tables before
  the UPSERT. Drop `--truncate` if you want to merge multiple extracts.
