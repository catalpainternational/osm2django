from django.contrib.gis import admin
from osmflex import models

# Register your models here.


class OsmFlexAdmin(admin.GISModelAdmin):
    list_display = ("osm_id", "osm_type", "name")
    list_filter = ("osm_type",)

class OsmWithSubtypeAdmin(admin.GISModelAdmin):
    list_display = ("osm_id", "osm_type", "osm_subtype", "name")
    list_filter = ("osm_type", "osm_subtype")

@admin.register(models.AmenityLine)
class AmenityLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.AmenityPoint)
class AmenityPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.AmenityPolygon)
class AmenityPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.BuildingPoint)
class BuildingPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.BuildingPolygon)
class BuildingPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.IndoorLine)
class IndoorLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.IndoorPoint)
class IndoorPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.IndoorPolygon)
class IndoorPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.InfrastructureLine)
class InfrastructureLineAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.InfrastructurePoint)
class InfrastructurePointAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.InfrastructurePolygon)
class InfrastructurePolygonAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.LandusePoint)
class LandusePointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.LandusePolygon)
class LandusePolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.LeisurePoint)
class LeisurePointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.LeisurePolygon)
class LeisurePolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.NaturalLine)
class NaturalLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.NaturalPoint)
class NaturalPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.NaturalPolygon)
class NaturalPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PlaceLine)
class PlaceLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PlacePoint)
class PlacePointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PlacePolygon)
class PlacePolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PoiLine)
class PoiLineAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.PoiPoint)
class PoiPointAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.PoiPolygon)
class PoiPolygonAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.PublicTransportLine)
class PublicTransportLineAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.PublicTransportPoint)
class PublicTransportPointAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.PublicTransportPolygon)
class PublicTransportPolygonAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.RoadLine)
class RoadLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.RoadPoint)
class RoadPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.RoadPolygon)
class RoadPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.ShopPoint)
class ShopPointAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.ShopPolygon)
class ShopPolygonAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.TrafficLine)
class TrafficLineAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.TrafficPoint)
class TrafficPointAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.TrafficPolygon)
class TrafficPolygonAdmin(OsmWithSubtypeAdmin):
    ...


@admin.register(models.Unitable)
class UnitableAdmin(admin.GISModelAdmin):
    ...


@admin.register(models.WaterLine)
class WaterLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.WaterPoint)
class WaterPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.WaterPolygon)
class WaterPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.Tags)
class TagsAdmin(admin.GISModelAdmin):
    ...
