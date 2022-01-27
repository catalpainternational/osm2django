# osm2django

Import OSM data to Django

OSM :heart: Django

## The Why

OpenStreetmap is a superb resource. Django is a superb ORM. But they have different views of data. Recent changes to the `osm2pgsql` tool, in particular the ability to flexibly define output, make it a lot easier to have Django-compatible imports

## How it works

This is a Django interface to models imported with `osm2pgsql`  and the `pgosm-flex` styles. After installing the dependencies and running the import, you get a set of nicely specified tables in an `osm` schema. From that schema you can import to parallel tables in this app.

### Prerequisites

Requires:
 - [osm2pgsql](https://github.com/openstreetmap/osm2pgsql), Build it from source as per [the docs](https://github.com/openstreetmap/osm2pgsql/blob/master/README.md#building)
 - [luarocks](https://luarocks.org/) can be installed from source or apt
 - luarocks: inifile via `sudo luarocks install inifile`
 - luarocks: luasql-postgres `sudo luarocks install luasql-postgres PGSQL_INCDIR=/usr/include/postgresql/`

There is a copy of the flex-config dir in this repo, so you do not need to clone them but the lua files are sourced from:

The original repo [rustprooflabs/pgosm-flex](https://github.com/rustprooflabs/pgosm-flex)
A fork in [joshbrooks/pgosm-flex](https://github.com/joshbrooks/pgosm-flex) added airports (for now) (PR submitted)

`osm2pgsql --version`

```pre
2022-01-26 14:40:57  osm2pgsql version 1.5.2 (1.5.2-15-g25a1e9d1)
Build: RelWithDebInfo
Compiled using the following library versions:
Libosmium 2.17.3
Proj [API 4] Rel. 6.3.1, February 10th, 2020
Lua 5.3.3
```

## Demo



## Constants

I tend to run in a docker container so the `PORT` here reflects that

```sh
export PASSWORD=post1234
export PORT=49154
export PGOSM_CONN_PG="postgresql://postgres:${PASSWORD}@localhost:${PORT}/postgres"
export PGOSM_CONN="postgresql://postgres:${PASSWORD}@localhost:${PORT}/postgres"
```

Run the container. Here it's using the latest postgis image and not fsync-ing for better performance

```sh
docker run --rm -d --name osm_import -e POSTGRES_PASSWORD=${PASSWORD} -p ${PORT}:5432 postgis/postgis:14-3.2 -c fsync=off
```

Wait for startup. One way to do so is to use `pg_isready`

```sh
pg_isready --host=localhost --port=${PORT}



```sh
# Create an "osm" schema
docker exec --user postgres osm_import psql -c "CREATE SCHEMA osm;"
```

```sh
# Constants for this particular import...
export PGOSM_DATE=`date -I`
export PGOSM_REGION='asia/east-timor'
export IMPORT_PBF="/media/josh/blackgate/osm/asia/east-timor-latest.osm.pbf"

# Clearly that won't work outside of here

# cd to the repo
cd path_to_repo/flex-config
# Run the import command

osm2pgsql \
    --number-processes=7 \
    --keep-coastlines \
    --output=flex --style=./run.lua \
    -d $PGOSM_CONN \
    ${IMPORT_PBF}
echo "Done"
```

## Copy to Django

The management command at `./manage.py import_from_pgosm_flex` inserts with update-on-conflict
