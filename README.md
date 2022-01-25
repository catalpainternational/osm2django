# osm2django

Import OSM data to Django

OSM :heart: Django

## The Why

OpenStreetmap is a superb resource. Django is a superb ORM. But they have different views of data. Recent changes to the `osm2pgsql` tool, in particular the ability to flexibly define output, make it a lot easier to have Django-compatible imports

## How it works

This is a Django interface to models imported with `osm2pgsql`  and the `pgosm-flex` styles. After installing the dependencies and running the import, you get a set of nicely specified tables in an `osm` schema. From that schema you can import to parallel tables in this app.

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
export PGOSM_DATE='2022-01-01'
export PGOSM_REGION='asia/east-timor'
export IMPORT_PBF="/media/josh/blackgate/osm/asia/east-timor-latest.osm.pbf"
export REPO="~/github/joshbrooks/pgosm-flex/flex-config-django"
# Clearly that won't work outside of here

# cd to the repo
cd $REPO
# Run the import command

osm2pgsql \
    --number-processes=7 \
    --keep-coastlines \
    --output=flex --style=./run.lua \
    -d $PGOSM_CONN \
    ${IMPORT_PBF}
echo "Done"
```
