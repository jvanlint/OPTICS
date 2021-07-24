# For PDF

import os
from datetime import timezone
from io import BytesIO
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm  # add this
from django.contrib.staticfiles import finders
from django.core import serializers
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# For PDF
from django.template.loader import get_template
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from xhtml2pdf import pisa

from .decorators import unauthenticated_user, allowed_users
from .forms import (
    CampaignForm,
    MissionForm,
    NewUserForm,
    PackageForm,
    ThreatForm,
    FlightForm,
    AircraftForm,
    TargetForm,
    SupportForm,
    WaypointForm,
    MissionImageryForm,
    ProfileForm,
    UserForm,
)
from .models import (
    Campaign,
    Mission,
    Package,
    Flight,
    Threat,
    Aircraft,
    Target,
    Support,
    Waypoint,
    MissionImagery,
)


def is_admin(user):
    return user.groups.filter(name="admin").exists()


def is_planner(user):
    return user.groups.filter(name="planner").exists()


def has_change_permission(self, request, obj=None):
    if obj is not None:
        if request.user.is_superuser:
            return True
        else:
            if obj.creator != request.user:
                return False
            else:
                return True


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # num_campaigns = Campaign.objects.all().count()

    num_missions = Mission.objects.count()

    context = {
        "num_campaigns": num_campaigns,
        "num_missions": num_missions,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


# Campaign Views
@login_required(login_url="login")
def campaign(request):
    campaigns = Campaign.objects.order_by("id")

    context = {"campaigns": campaigns, "isAdmin": is_admin(request.user)}

    return render(request, "campaign/campaign.html", context=context)


@login_required(login_url="login")
def campaign_detail(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missions = campaign.mission_set.all().order_by("number")

    campaign.refresh_from_db()

    context = {
        "campaign_Object": campaign,
        "mission_Object": missions,
        "isAdmin": is_admin(request.user),
    }

    return render(request, "campaign/campaign_detail.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def campaign_create(request):
    form = CampaignForm(initial={"creator": request.user.id})

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully created.")
            return HttpResponseRedirect("/airops/campaign")

    context = {"form": form}
    return render(request, "campaign/campaign_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def campaign_update(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    form = CampaignForm(instance=campaign)
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully updated.")
            return HttpResponseRedirect(returnURL)

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "campaign/campaign_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def campaign_delete(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        campaign.delete()
        messages.success(request, "Campaign successfully deleted.")
        return HttpResponseRedirect("/airops/campaign")

    context = {"item": campaign, "returnURL": returnURL}
    return render(request, "campaign/campaign_delete.html", context=context)


# Mission Views


@login_required(login_url="login")
@never_cache
def mission(request, link_id):
    mission = Mission.objects.get(id=link_id)
    packages = mission.package_set.all()
    threat = mission.threat_set.all()
    target = mission.target_set.all()
    support = mission.support_set.all()
    imagery = mission.missionimagery_set.all()

    context = {
        "mission_object": mission,
        "package_object": packages,
        "threat_object": threat,
        "target_object": target,
        "support_object": support,
        "imagery_object": imagery,
        "isAdmin": is_admin(request.user),
        "isPlanner": is_planner(request.user),
        "user_timezone": request.user.profile.timezone,
    }
    return render(request, "mission/mission_detail.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_create(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missionCount = campaign.mission_set.count() + 1
    returnURL = request.GET.get("returnUrl")

    form = MissionForm(initial={"campaign": campaign, "number": missionCount})
    # form.base_fields['number'].initial = missionCount

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Mission date and time are combined in the form's clean function
            # https://stackoverflow.com/questions/53742129/how-do-you-modify-form-data-before-saving-it-while-using-djangos-createview

            # form.mission_date=form.mission_date.replace(tzinfo=timezone.utc)
            '''
            combine the time and date responses and create a date/time to be 
            saved in the mission datetime field.
            Do this also for the update view below (extract to a function)
            Also will need to do the reverse for the view of this field.
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
            https://www.programiz.com/python-programming/datetime
            https://realpython.com/python39-new-features/#proper-time-zone-support
            check settings.py for correct time format
            https://docs.djangoproject.com/en/3.2/ref/settings/#time-input-formats
            https://docs.djangoproject.com/en/3.2/ref/models/fields/#datetimefield
            http://diveintohtml5.info/forms.html
            mission_data is datetime UTC+10 (settings.py default timezone)
            mission_time is string
            mission_game_time is string
            mission_game_date is datetime UTC+10
            '''
            form.save(commit=True)
            return HttpResponseRedirect("/airops/campaign/" + str(link_id))

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "mission/mission_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_update(request, link_id):
    mission = Mission.objects.get(id=link_id)
    form = MissionForm(instance=mission)
    returnURL = request.GET.get("returnUrl")
    
    image_url = request.build_absolute_uri(mission.campaign.campaignImage.url)
    
    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES, instance=mission)
        
        if form.is_valid():
            saved_obj = form.save(commit=True)
            # Post to Discord.
            if saved_obj.notify_discord:
                mission.create_discord_event(image_url, request)
            return HttpResponseRedirect(returnURL)

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "mission/mission_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_delete(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")
    campaignID = mission.campaign.id

    if request.method == "POST":
        mission.delete()
        return HttpResponseRedirect("/airops/campaign/" + str(campaignID))

    context = {"item": mission, "returnURL": returnURL}
    return render(request, "mission/mission_delete.html", context=context)


# Package Views


@login_required(login_url="login")
@never_cache
def package(request, link_id):
    package = Package.objects.get(id=link_id)
    flights = package.flight_set.all()

    context = {"package_Object": package, "flight_Object": flights}
    return render(request, "package/package_detail.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def package_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    form = PackageForm(initial={"mission": mission})
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/mission/" + str(link_id))

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "package/package_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def package_update(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    form = PackageForm(instance=package)
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES, instance=package)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {"form": form, "link": missionID, "returnURL": returnURL}
    return render(request, "package/package_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def package_delete(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        package.delete()
        return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"item": package, "returnURL": returnURL}
    return render(request, "package/package_delete.html", context=context)


# Threat Views
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")
    form = ThreatForm(initial={"mission": mission})

    if request.method == "POST":
        form = ThreatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/mission/" + str(link_id))

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "threat/threat_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_update(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id
    form = ThreatForm(instance=threat)
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        form = ThreatForm(request.POST, request.FILES, instance=threat)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "threat/threat_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_delete(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id

    if request.method == "POST":
        threat.delete()
        return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"item": threat}
    return render(request, "threat/threat_delete.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_copy(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id

    new_threat_instance = Threat(
        mission=threat.mission,
        threat_name=threat.threat_name + "(Copy)",
        name=threat.name,
        threat_type=threat.threat_type,
        description=threat.description,
    )
    new_threat_instance.save()

    return HttpResponseRedirect("/airops/mission/" + str(missionID))


# Mission Imagery Views


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_imagery_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = MissionImageryForm(initial={"mission": mission})

    if request.method == "POST":
        form = MissionImageryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/mission/" + str(link_id))

    context = {"form": form, "link": link_id}
    return render(request, "missionImagery/missionImagery_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_imagery_update(request, link_id):
    imagery = MissionImagery.objects.get(id=link_id)

    missionID = imagery.mission.id
    form = MissionImageryForm(instance=imagery)

    if request.method == "POST":
        form = MissionImageryForm(request.POST, request.FILES, instance=imagery)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"form": form, "link": missionID}
    return render(request, "missionImagery/missionImagery_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_imagery_delete(request, link_id):
    imagery = MissionImagery.objects.get(id=link_id)
    missionID = imagery.mission.id
    if request.method == "POST":
        imagery.delete()
        return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"item": imagery}
    return render(request, "missionImagery/missionImagery_delete.html", context=context)


### Flight Views ###


@login_required(login_url="login")
@never_cache
def flight(request, link_id):
    flight = Flight.objects.get(id=link_id)
    aircraft = flight.aircraft_set.all().order_by("-flight_lead", "type", "pilot")
    waypoints = flight.waypoint_set.all().order_by("number")
    targets = flight.targets.all()

    context = {
        "flight_Object": flight,
        "aircraft_Object": aircraft,
        "waypoint_Object": waypoints,
        "target_Object": targets,
    }
    return render(request, "flight/flight_detail.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_create(request, link_id):
    package = Package.objects.get(id=link_id)

    # Filter the target field to just targets from the mission.
    target = Target.objects.filter(mission=package.mission.id)

    form = FlightForm(target, initial={"package": package})

    if request.method == "POST":
        form = FlightForm(target, request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/package/" + str(link_id))

    context = {"form": form, "link": link_id}
    return render(request, "flight/flight_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_update(request, link_id):
    flight = Flight.objects.get(id=link_id)
    packageID = flight.package.id
    returnURL = request.GET.get("returnUrl")

    # Filter the target field to just targets from the mission.
    target = Target.objects.filter(mission=flight.package.mission.id)

    form = FlightForm(target, instance=flight)

    if request.method == "POST":
        form = FlightForm(target, request.POST, instance=flight)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "flight/flight_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_delete(request, link_id):
    flight = Flight.objects.get(id=link_id)
    packageID = flight.package.id
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        flight.delete()
        return HttpResponseRedirect("/airops/package/" + str(packageID))

    context = {"item": flight, "returnURL": returnURL}
    return render(request, "flight/flight_delete.html", context=context)


### Aircraft Views ###


@login_required(login_url="login")
def aircraft(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)

    context = {"aircraftObject": aircraft}
    return render(request, "aircraft/aircraft_detail.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def aircraft_create(request, link_id):
    flight = Flight.objects.get(id=link_id)

    # Filter the flights field to just targets from the mission.
    flights = Flight.objects.filter(package=flight.package.id)

    form = AircraftForm(flights, initial={"flight": flight})

    if request.method == "POST":
        form = AircraftForm(flights, request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/flight/" + str(link_id))

    context = {"form": form, "link": link_id}
    return render(request, "aircraft/aircraft_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def aircraft_update(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id

    # Filter the flights field to just targets from the mission.
    flights = Flight.objects.filter(package=aircraft.flight.package.id)

    form = AircraftForm(flights, instance=aircraft)

    if request.method == "POST":
        form = AircraftForm(flights, request.POST, request.FILES, instance=aircraft)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect("/airops/flight/" + str(flightID))

    context = {"form": form, "link": flightID}
    return render(request, "aircraft/aircraft_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def aircraft_delete(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id

    if request.method == "POST":
        aircraft.delete()
        return HttpResponseRedirect("/airops/flight/" + str(flightID))

    context = {"item": aircraft}
    return render(request, "aircraft/aircraft_delete.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def aircraft_copy(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id

    new_aircraft_instance = Aircraft(
        type=aircraft.type,
        flight=aircraft.flight,
    )
    new_aircraft_instance.save()

    return HttpResponseRedirect("/airops/flight/" + str(flightID))


### Target Views ###


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")
    form = TargetForm(initial={"mission": mission})

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/mission/" + str(link_id))

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "target/target_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_update(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id
    form = TargetForm(instance=target)
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES, instance=target)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"form": form, "link": missionID, "returnURL": returnURL}
    return render(request, "target/target_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_delete(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        target.delete()
        return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"item": target}
    return render(request, "target/target_delete.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_copy(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id

    new_target_instance = Target(
        mission=target.mission,
        name=target.name + "(Copy)",
        lat=target.lat,
        long=target.long,
        elev=target.elev,
        notes=target.notes,
    )
    new_target_instance.save()

    return HttpResponseRedirect("/airops/mission/" + str(missionID))


### Support Views ###


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")
    form = SupportForm(initial={"mission": mission})

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/mission/" + str(link_id))

    context = {"form": form, "link": link_id, "returnURL": returnURL}
    return render(request, "support/support_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_update(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = support.mission.id
    form = SupportForm(instance=support)
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES, instance=support)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"form": form, "link": missionID, "returnURL": returnURL}
    return render(request, "support/support_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_delete(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = support.mission.id

    if request.method == "POST":
        support.delete()
        return HttpResponseRedirect("/airops/mission/" + str(missionID))

    context = {"item": support}
    return render(request, "support/support_delete.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_copy(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = support.mission.id

    new_support_instance = Support(
        mission=support.mission,
        callsign=support.callsign + "(Copy)",
        support_type=support.support_type,
        player_name=support.player_name,
        frequency=support.frequency,
        tacan=support.tacan,
        altitude=support.altitude,
        speed=support.speed,
        brc=support.brc,
        icls=support.icls,
        notes=support.notes,
    )
    new_support_instance.save()

    return HttpResponseRedirect("/airops/mission/" + str(missionID))


# Waypoint Views
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def waypoint_create(request, link_id):
    flight = Flight.objects.get(id=link_id)

    form = WaypointForm(initial={"flight": flight})

    if request.method == "POST":
        form = WaypointForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect("/airops/flight/" + str(link_id))

    context = {"form": form, "link": link_id}
    return render(request, "waypoint/waypoint_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def waypoint_update(request, link_id):
    waypoint = Waypoint.objects.get(id=link_id)
    flightID = waypoint.flight.id
    form = WaypointForm(instance=waypoint)

    if request.method == "POST":
        form = WaypointForm(request.POST, request.FILES, instance=waypoint)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect("/airops/flight/" + str(flightID))

    context = {"form": form, "link": flightID}
    return render(request, "waypoint/waypoint_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def waypoint_delete(request, link_id):
    waypoint = Waypoint.objects.get(id=link_id)
    flightID = waypoint.flight.id

    if request.method == "POST":
        waypoint.delete()
        return HttpResponseRedirect("/airops/flight/" + str(flightID))

    context = {"item": waypoint}
    return render(request, "waypoint/waypoint_delete.html", context=context)


# Other Views


def dashboard(request):
    context = {}
    return render(request, "dashboard/dashboard.html", context)


@unauthenticated_user
def register_request(request):
    if request.user.is_authenticated:
        return redirect("campaign")
    else:
        if request.method == "POST":
            user_form = NewUserForm(request.POST)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile_form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return HttpResponseRedirect("/airops/campaign")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        user_form = NewUserForm
        profile_form = ProfileForm
        return render(
            request=request,
            template_name="dashboard/register.html",
            context={"register_form": user_form, "profile_form": profile_form},
        )


@unauthenticated_user
@csrf_protect
def login_request(request):
    if request.user.is_authenticated:
        return redirect("campaign")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, "You are now logged in as " + username + ".")
                    return redirect("campaign")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(
            request=request,
            template_name="dashboard/login.html",
            context={"login_form": form},
        )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return HttpResponseRedirect("/airops/campaign")


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "dashboard/change_password.html", {"form": form})


# PDF Render


def fetch_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    print("Starting...")
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/
        print("Media Root:" + mRoot)

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            print("URI: " + uri)
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    print("Path: " + path)
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # pdf = pisa.CreatePDF(html, dest=result, link_callback=fetch_resources)
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def download_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {"mission_object": mission, "flight_object": flight}
    pdf = render_to_pdf("mission_card/pdf_template.html", data)
    response = HttpResponse(pdf, content_type="application/pdf")
    filename = "missioncard.pdf"
    content = "attachment; filename=%s" % (filename)
    response["Content-Disposition"] = content
    return response


def view_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)
    packages = mission.package_set.all()
    aircraft = flight.aircraft_set.all().order_by("-flight_lead")
    waypoints = flight.waypoint_set.all()
    supports = mission.support_set.all()
    targets = flight.targets.all()
    threats = mission.threat_set.all()
    # threat_details = threats.threat_name.harm_code

    target_urls = []
    if targets:
        for target in targets:
            if target.target_image:
                target_urls.append(request.build_absolute_uri(target.target_image.url))

    data = {
        "mission_object": mission,
        "flight_object": flight,
        "packages_object": packages,
        "aircraft_object": aircraft,
        "waypoints_object": waypoints,
        "support_object": supports,
        "target_object": targets,
        "threat_object": threats,
        "urls": target_urls,
    }

    pdf = render_to_pdf("mission_card/pdf_template.html", data)
    return HttpResponse(pdf, content_type="application/pdf")


def new_view_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {
        "mission_object": mission,
        "flight_object": flight,
    }

    template_path = "mission_card/pdf_template.html"
    context = data
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="mission_card.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=fetch_resources)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required(login_url="login")
def mission_signup(request, link_id):  # link_id is the mission ID
    mission = Mission.objects.get(id=link_id)
    packages = mission.package_set.all()

    has_seat = 0
    package_list = serializers.serialize("python", packages)
    for package in package_list:
        has_seat += (
            Aircraft.objects.filter(flight__package__id=package["pk"])
            .filter(pilot=request.user)
            .count()
        )
        has_seat += (
            Aircraft.objects.filter(flight__package__id=package["pk"])
            .filter(rio_wso=request.user)
            .count()
        )
    campaign = Campaign.objects.get(mission=mission)
    is_owner = campaign.creator == request.user
    context = {
        "mission_object": mission,
        "package_object": packages,
        "has_seat": has_seat,
        "is_owner": is_owner,
    }

    return render(request, "mission/mission_signup.html", context)


@login_required(login_url="login")
def mission_signup_update(request, link_id, seat_id):
    returnURL = request.GET.get("returnUrl")
    aircraft = Aircraft.objects.get(pk=link_id)
    if seat_id == 1:
        aircraft.pilot = request.user
    else:
        aircraft.rio_wso = request.user

    aircraft.save()

    return HttpResponseRedirect(returnURL)


@login_required(login_url="login")
def mission_signup_remove(request, link_id, seat_id):
    returnURL = request.GET.get("returnUrl")
    aircraft = Aircraft.objects.get(pk=link_id)
    if seat_id == 1:
        aircraft.pilot = None
    else:
        aircraft.rio_wso = None

    aircraft.save()

    return HttpResponseRedirect(returnURL)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("campaign")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request,
        "profiles/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
