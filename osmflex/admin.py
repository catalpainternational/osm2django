from django.contrib.gis import admin
from osmflex import models

# Register your models here.


class OsmFlexAdmin(admin.GISModelAdmin):
    def get_list_filter(self, request):
        fields = [n.name for n in self.model._meta.fields]
        list_filters = ["osm_type", "osm_subtype"]
        return [f for f in list_filters if f in fields]

    def get_list_display(self, request):
        list_display = ("osm_id", "osm_type", "osm_subtype", "name")
        fields = [n.name for n in self.model._meta.fields]
        return [f for f in list_display if f in fields]


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
class InfrastructureLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.InfrastructurePoint)
class InfrastructurePointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.InfrastructurePolygon)
class InfrastructurePolygonAdmin(OsmFlexAdmin):
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
class PoiLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PoiPoint)
class PoiPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PoiPolygon)
class PoiPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PublicTransportLine)
class PublicTransportLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PublicTransportPoint)
class PublicTransportPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.PublicTransportPolygon)
class PublicTransportPolygonAdmin(OsmFlexAdmin):
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
class ShopPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.ShopPolygon)
class ShopPolygonAdmin(OsmFlexAdmin):
    ...


@admin.register(models.TrafficLine)
class TrafficLineAdmin(OsmFlexAdmin):
    ...


@admin.register(models.TrafficPoint)
class TrafficPointAdmin(OsmFlexAdmin):
    ...


@admin.register(models.TrafficPolygon)
class TrafficPolygonAdmin(OsmFlexAdmin):
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
