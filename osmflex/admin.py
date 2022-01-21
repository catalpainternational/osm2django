from django.contrib import admin
from osmflex import models

# Register your models here.

@admin.register(models.AmenityLine)
class AmenityLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.AmenityPoint)
class AmenityPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.AmenityPolygon)
class AmenityPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.BuildingPoint)
class BuildingPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.BuildingPolygon)
class BuildingPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.IndoorLine)
class IndoorLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.IndoorPoint)
class IndoorPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.IndoorPolygon)
class IndoorPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.InfrastructureLine)
class InfrastructureLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.InfrastructurePoint)
class InfrastructurePointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.InfrastructurePolygon)
class InfrastructurePolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.LandusePoint)
class LandusePointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.LandusePolygon)
class LandusePolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.LeisurePoint)
class LeisurePointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.LeisurePolygon)
class LeisurePolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.NaturalLine)
class NaturalLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.NaturalPoint)
class NaturalPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.NaturalPolygon)
class NaturalPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PlaceLine)
class PlaceLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PlacePoint)
class PlacePointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PlacePolygon)
class PlacePolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PoiLine)
class PoiLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PoiPoint)
class PoiPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PoiPolygon)
class PoiPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PublicTransportLine)
class PublicTransportLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PublicTransportPoint)
class PublicTransportPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.PublicTransportPolygon)
class PublicTransportPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.RoadLine)
class RoadLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.RoadPoint)
class RoadPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.RoadPolygon)
class RoadPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.ShopPoint)
class ShopPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.ShopPolygon)
class ShopPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.TrafficLine)
class TrafficLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.TrafficPoint)
class TrafficPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.TrafficPolygon)
class TrafficPolygonAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Unittable)
class UnittableAdmin(admin.ModelAdmin):
    ...

@admin.register(models.WaterLine)
class WaterLineAdmin(admin.ModelAdmin):
    ...

@admin.register(models.WaterPoint)
class WaterPointAdmin(admin.ModelAdmin):
    ...

@admin.register(models.WaterPolygon)
class WaterPolygonAdmin(admin.ModelAdmin):
    ...
