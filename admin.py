from django.contrib import admin

# Register your models here.

from .models import Campaign, Mission, Package, Flight, Aircraft, Status, Airframe, Terrain, Threat, Target, Support, Waypoint
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Define the admin class


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'status')
    list_filter = ('start_date', 'status')


# Register the admin class with the associated model
admin.site.register(Campaign, CampaignAdmin)


class PackageInline(admin.TabularInline):
    model = Package
    extra = 3


class MissionAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'mission_date', 'get_campaign')
    inlines = [PackageInline]

    def get_campaign(self, obj):
        return obj.campaign.name
    get_campaign.short_description = 'Campaign'


admin.site.register(Mission, MissionAdmin)


class FlightInline(admin.TabularInline):
    model = Flight
    extra = 3


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_mission', 'get_campaign')
    inlines = [FlightInline]

    def get_mission(self, obj):
        return obj.mission.name
    get_mission.short_description = 'Mission'

    def get_campaign(self, obj):
        return obj.mission.campaign.name
    get_campaign.short_description = 'Campaign'


admin.site.register(Package, PackageAdmin)


class FlightAdmin(admin.ModelAdmin):
    list_display = ('callsign', 'get_package', 'get_mission', 'get_campaign')

    def get_package(self, obj):
        return obj.package.name
    get_package.short_description = 'Package'

    def get_mission(self, obj):
        return obj.package.mission.name
    get_mission.short_description = 'Mission'

    def get_campaign(self, obj):
        return obj.package.mission.campaign.name
    get_campaign.short_description = 'Campaign'


admin.site.register(Flight, FlightAdmin)


class AircraftAdmin(admin.ModelAdmin):
    list_display = ('type', 'get_flight')

    def get_flight(self, obj):
        return obj.flight.callsign
    get_flight.short_description = 'Flight'


admin.site.register(Aircraft, AircraftAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Status, StatusAdmin)


class TerrainAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Terrain, TerrainAdmin)


class AirframeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Airframe, AirframeAdmin)


class ThreatAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Threat, ThreatAdmin)


class TargetAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Target, TargetAdmin)


class SupportAdmin(admin.ModelAdmin):
    list_display = ('callsign',)


admin.site.register(Support, SupportAdmin)


class WaypointAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Waypoint, WaypointAdmin)


class MyUserAdmin(admin.ModelAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
        group.short_description = 'Groups'

    list_display = ['username', 'first_name', 'last_name',
                    'is_active', 'last_login', 'group']


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
