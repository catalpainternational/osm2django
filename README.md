# osm2django

## Installing

Clone the repo and `poetry install`

Or `pip install osmflex`

## Import OSM data to Django

OSM :heart: Django

```
(env) josh@carbonite:~/github/catalpainternational/openly_dird$ ./manage.py run_osm2pgsql ~/Downloads/papua-new-guinea-latest.osm.pbf 
Creating the `osm` schema
Running Import of /home/josh/Downloads/papua-new-guinea-latest.osm.pbf
This may take a few minutes...
Running Import of /home/josh/Downloads/papua-new-guinea-latest.osm.pbf complete
To insert/update the Django tables, please run `import_from_pgosmflex`
You can drop the osm schema after that command
(env) josh@carbonite:~/github/catalpainternational/openly_dird$ ./manage.py import_from_pgosmflex
Importing data to osmflex_waterline

    INSERT INTO "osmflex_waterline"
        ("osm_id","osm_type","name","geom","layer","tunnel","bridge","boat","osm_subtype")
    SELECT "osm_id","osm_type","name","geom","layer","tunnel","bridge","boat","osm_subtype" FROM "osm"."water_line"
    ON CONFLICT
        ON CONSTRAINT "osmflex_waterline_pkey"
        DO UPDATE SET
        "osm_id" = Excluded."osm_id","osm_type" = Excluded."osm_type","name" = Excluded."name","geom" = Excluded."geom","layer" = Excluded."layer","tunnel" = Excluded."tunnel","bridge" = Excluded."bridge","boat" = Excluded."boat","osm_subtype" = Excluded."osm_subtype"
        WHERE "osmflex_waterline".osm_id = Excluded.osm_id
    
Importing data to osmflex_roadpoint
```
    INSERT INTO "osmflex_roadpoint"
        ("osm_id","osm_type","name","geom","ref","maxspeed","layer","tunnel","bridge","oneway","access")
    SELECT "osm_id","osm_type","name","geom","ref","maxspeed","layer","tunnel","bridge","oneway","access" FROM "osm"."road_point"
    ON CONFLICT
        ON CONSTRAINT "osmflex_roadpoint_pkey"
        DO UPDATE SET
        "osm_id" = Excluded."osm_id","osm_type" = Excluded."osm_type","name" = Excluded."name","geom" = Excluded."geom","ref" = Excluded."ref","maxspeed" = Excluded."maxspeed","layer" = Excluded."layer","tunnel" = Excluded."tunnel","bridge" = Excluded."bridge","oneway" = Excluded."oneway","access" = Excluded."access"
        WHERE "osmflex_roadpoint".osm_id = Excluded.osm_id
    
... (other tables)
```

```ipython
In [1]: from osmflex import models

In [2]: models.AmenityPoint.objects.all()
Out[2]: <QuerySet [<AmenityPoint: vending_machine(8106929355)>, <AmenityPoint: toilets(2932913055)>, <AmenityPoint: shower(2932913054)>, <AmenityPoint: drinking_water(2932913053)>, <AmenityPoint: Magesubu Cemetery(2932834661)>, <AmenityPoint: Gegela Cemetery(2932834660)>, <AmenityPoint: Watertank Simon & Elsi(2943488679)>, <AmenityPoint: Teachers Watertank(2943486625)>, <AmenityPoint: Tubetube School(2540118236)>, <AmenityPoint: Teacher Watertank(2932988387)>, <AmenityPoint: toilets(2585430641)>, <AmenityPoint: toilets(2574655335)>, <AmenityPoint: Dawasi Cemetery(2943488655)>, <AmenityPoint: Pastors Watertank(2943488638)>, <AmenityPoint: (old)(2943488670)>, <AmenityPoint: drinking_water(2943488669)>, <AmenityPoint: fountain(2585422282)>, <AmenityPoint: toilets(2943488667)>, <AmenityPoint: shower(2943488668)>, <AmenityPoint: Watertank Lucia & David(2932818615)>, '...(remaining elements truncated)...']>

In [3]: 
```



## The Why

OpenStreetmap is a superb resource. Django is a superb ORM. But they have different views of data. Recent changes to the `osm2pgsql` tool, in particular the ability to flexibly define output, make it a lot easier to have Django-compatible imports

## How it works

This is a Django interface to models imported with `osm2pgsql`  and the `pgosm-flex` styles. After installing the dependencies and running the import, you get a set of nicely specified tables in an `osm` schema. From that schema you can import to parallel tables in this app.

### Prerequisites

Requires:
 - [osm2pgsql](https://github.com/openstreetmap/osm2pgsql), Build it from source as per [the docs](https://github.com/openstreetmap/osm2pgsql/blob/master/README.md#building)

There is a copy of the flex-config dir in this repo. The `lua` files are sourced from [rustprooflabs/pgosm-flex](https://github.com/rustprooflabs/pgosm-flex)

`osm2pgsql --version`

```pre
2022-01-26 14:40:57  osm2pgsql version 1.5.2 (1.5.2-15-g25a1e9d1)
Build: RelWithDebInfo
Compiled using the following library versions:
Libosmium 2.17.3
Proj [API 4] Rel. 6.3.1, February 10th, 2020
Lua 5.3.3
```

## Building

poetry version patch
poetry build
poetry publish

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
