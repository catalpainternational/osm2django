"""SQL generators for the pgosm-flex → Django import step.

These render `psycopg2.sql.Composed` fragments; execute them via
`connection.cursor().execute(str(sql), ...)`. They are used by
`osmflex.management.commands.import_from_pgosmflex` but are exported as
public utilities so downstream apps can build their own import pipelines
on top of the same primitives.
"""

from django.db import models
from psycopg2 import sql


def truncate_sql(model: type[models.Model]) -> sql.Composed:
    """Render ``TRUNCATE {table} CASCADE`` for the given Django model class.

    BE CAREFUL: `CASCADE` will drop rows in any table with a foreign key
    into `model`. Used by ``import_from_pgosmflex --truncate`` to clear
    the destination table before the UPSERT.
    """
    return sql.SQL("TRUNCATE {table} CASCADE;").format(table=sql.Identifier(model._meta.db_table))


def upsert_sql(model: type[models.Model], exclude_fields: list[str] | None = None) -> sql.Composed:
    """Render an ``INSERT ... ON CONFLICT DO UPDATE`` from the parallel source table.

    pgosm-flex writes into schema ``osm.<source_table>`` (e.g. ``osm.road_line``).
    This renders a Django-model-side UPSERT pulling from that source into the
    Django-managed ``osmflex_<model_name>`` table, using ``osm_id`` as the
    conflict key.

    The source table name is derived from ``model._meta.db_table`` by stripping
    the ``osmflex_`` prefix and re-injecting underscores that Django's model
    naming rules had stripped:

    ==========================  =================
    Django table                Source table (osm.*)
    ==========================  =================
    ``osmflex_roadline``        ``road_line``
    ``osmflex_publictransport`` ``public_transport``
    ``osmflex_roadmajor``       ``road_major``
    ==========================  =================

    ``exclude_fields`` drops named columns from both the INSERT column list and
    the ``DO UPDATE SET`` clause — useful when the source table is missing a
    column that the Django model has (e.g. a locally-computed field).

    The generated statement expects an existing primary-key constraint named
    ``{db_table}_pkey``, which is Django's default naming.
    """
    table = sql.Identifier(model._meta.db_table)
    field_names = [f.db_column or f.get_attname() for f in model._meta.fields]

    for ex in exclude_fields or []:
        if ex in field_names:
            field_names.remove(ex)

    fields = sql.SQL(",").join([sql.Identifier(f) for f in field_names])

    source_table = sql.Identifier(
        model._meta.db_table.replace("osmflex_", "")
        .replace("point", "_point")
        .replace("line", "_line")
        .replace("polygon", "_polygon")
        .replace("publictransport", "public_transport")
        .replace("roadmajor", "road_major")
    )

    update_clause = sql.SQL("DO UPDATE SET\n\t") + sql.SQL(",").join([sql.Identifier(f) + sql.SQL(" = Excluded.") + sql.Identifier(f) for f in field_names])

    statement = sql.SQL(
        """
    INSERT INTO {table}
        ({fields})
    SELECT {fields} FROM {source_schema}.{source_table}
    ON CONFLICT
        ON CONSTRAINT {constraint}
        {update_clause}
        WHERE {table}.osm_id = Excluded.osm_id
    """
    ).format(
        table=table,
        fields=fields,
        source_table=source_table,
        update_clause=update_clause,
        source_schema=sql.Identifier("osm"),
        constraint=sql.Identifier(f"{model._meta.db_table}_pkey"),
    )

    return statement
