# osm2django
Import OSM data to Django


## How it works

This is a Django interface to models imported with` osm2pgsql`


```sh
export PASSWORD=post1234
export PORT=49154
export PGOSM_CONN_PG="postgresql://postgres:${PASSWORD}@localhost:${PORT}/postgres"
export PGOSM_CONN="postgresql://postgres:${PASSWORD}@localhost:${PORT}/postgres"
docker run --rm -d --name osm_import -e POSTGRES_PASSWORD=${PASSWORD} -p ${PORT}:5432 postgis/postgis:14-3.2 -c fsync=off
# Wait for startup
sleep 10
pg_isready --host=localhost --port=${PORT}
# Create an "osm" schema
# docker exec --user postgres osm_import psql -c "CREATE SCHEMA osm;"
export PGOSM_DATE='2022-01-01'
export PGOSM_REGION='asia/east-timor'
# cd to the repo
cd ~/github/joshbrooks/pgosm-flex/flex-config-django
# Run the import command

# The important thigs: Share a connection string to your Django db and the Lua config. should match the Django model definitions!

# Skip the "unitable" and "tags" tables as these can be very big + not so useful
export PGOSM_LAYERSET=dird

osm2pgsql \
    --number-processes=7 \
    --keep-coastlines \
    --output=flex --style=./run.lua \
    -d $PGOSM_CONN \
    /media/josh/blackgate/osm/asia/east-timor-latest.osm.pbf
echo "Done"
```
