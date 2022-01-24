from inspect import isfunction
from typing import Any, Callable, Dict, Optional
import warnings
import osmium
from dataclasses import asdict, is_dataclass, is_dataclass
from pyinstrument import Profiler

wkbfab = osmium.geom.WKBFactory()

from .models import get_model


def to_instance(osmthing):

    for model in get_model(osmthing):

        try:
            fields = {}

            for inherited in model.mro():
                function = getattr(inherited, "from_osm", None)  # type: Optional[Callable[[Any], Dict[str, Any]]]
                if function is not None:
                    result = function(osmthing)
                    if is_dataclass(result):
                        result = asdict(result)
                    fields.update(result)
                if not hasattr(inherited, "_meta"):
                    continue
                for field in inherited._meta.fields:
                    field_function = getattr(field, "from_osm", None)
                    if field_function is None:
                        continue
                    try:
                        result = field_function(osmthing)
                    except Exception as E:
                        raise
                    fields[field.name] = result
            try:
                model, created = model.objects.update_or_create(osm_id=osmthing.id, defaults=fields)

            except Exception as E:
                # warnings.warn(f"{E}")
                raise

        except Exception as E:
            # warnings.warn(f"{E}")
            raise


class ImportThings(osmium.SimpleHandler):
    def node(self, node):
        if not len(node.tags):
            return
        return to_instance(osmthing=node)

    def way(self, way):
        return to_instance(osmthing=way)

    def area(self, area):
        return to_instance(osmthing=area)


def test():

    p = Profiler()
    p.start()
    try:
        i = ImportThings()
        i.apply_file("/media/josh/blackgate/osm/asia/east-timor-latest.osm.pbf")
    finally:
        p.stop()
        p.open_in_browser()
