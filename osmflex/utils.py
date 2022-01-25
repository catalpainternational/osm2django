from django.db import models
from psycopg2 import sql


def upsert_sql(model: models.Model):
    """
    Generates an UPSERT (update-on-conflict) statement
    to import from the "osm" schema which is the default
    import target of pgosm-flex
    """

    table = sql.Identifier(model._meta.db_table)
    field_names = [f.db_column or f.get_attname() for f in model._meta.fields]
    fields = sql.SQL(",").join([sql.Identifier(f.db_column or f.get_attname()) for f in model._meta.fields])

    # TODO: Address source tables with additional '_' in them (power I think?)
    source_table = sql.Identifier(
        model._meta.db_table.replace("osmflex_", "")
        .replace("point", "_point")
        .replace("line", "_line")
        .replace("polygon", "_polygon")
        .replace("publictransport", "public_transport")
        .replace("roadmajor", "road_major")
    )

    # This is the update clause...
    update_clause = sql.SQL("DO UPDATE SET\n\t") + sql.SQL(",").join(
        [sql.Identifier(f) + sql.SQL(" = Excluded.") + sql.Identifier(f) for f in field_names]
    )

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
