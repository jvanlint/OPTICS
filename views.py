from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode

from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm  # add this
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_protect

from .models import Campaign, Mission, Package, Flight, Threat, Aircraft, Target, Support, Waypoint, MissionImagery, ThreatReference
from .forms import CampaignForm, MissionForm, NewUserForm, PackageForm, ThreatForm, FlightForm, AircraftForm, TargetForm, SupportForm, WaypointForm, MissionImageryForm
# For PDF
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings

from io import BytesIO
import os

from .decorators import unauthenticated_user, allowed_users


def is_admin(user):
    return user.groups.filter(name='admin').exists()


def is_planner(user):
    return user.groups.filter(name='planner').exists()


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
    # num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_missions = Mission.objects.count()

    context = {
        'num_campaigns': num_campaigns,
        'num_missions': num_missions,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Campaign Views
@login_required(login_url='login')
def campaign(request):
    campaigns = Campaign.objects.order_by('id')

    context = {'campaigns': campaigns, 'isAdmin': is_admin(request.user)}

    return render(request, 'campaign/campaign.html', context=context)


@login_required(login_url='login')
def campaign_detail(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missions = campaign.mission_set.all().order_by('number')

    campaign.refresh_from_db()

    context = {'campaign_Object': campaign, 'mission_Object': missions,
               'isAdmin': is_admin(request.user)}

    return render(request, 'campaign/campaign_detail.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def campaign_create(request):
    form = CampaignForm(initial={'creator': request.user.id})

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully created.")
            return HttpResponseRedirect('/airops/campaign')

    context = {'form': form}
    return render(request, 'campaign/campaign_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def campaign_update(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    form = CampaignForm(instance=campaign)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = CampaignForm(
            request.POST, request.FILES, instance=campaign)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully updated.")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'campaign/campaign_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def campaign_delete(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        campaign.delete()
        messages.success(request, "Campaign successfully deleted.")
        return HttpResponseRedirect('/airops/campaign')

    context = {'item': campaign, 'returnURL': returnURL}
    return render(request, 'campaign/campaign_delete.html', context=context)

# Mission Views


@login_required(login_url='login')
@never_cache
def mission(request, link_id):
    mission = Mission.objects.get(id=link_id)
    packages = mission.package_set.all()
    threat = mission.threat_set.all()
    target = mission.target_set.all()
    support = mission.support_set.all()
    imagery = mission.missionimagery_set.all()

    context = {'mission_object': mission,
               'package_object': packages, 'threat_object': threat, 'target_object': target, 'support_object': support, 'imagery_object': imagery, 'isAdmin': is_admin(request.user), 'isPlanner': is_planner(request.user)}
    return render(request, 'mission/mission_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def mission_create(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missionCount = campaign.mission_set.count() + 1
    returnURL = request.GET.get('returnUrl')

    form = MissionForm(initial={'campaign': campaign, 'number': missionCount})
    # form.base_fields['number'].initial = missionCount

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/campaign/' + str(link_id))

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'mission/mission_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def mission_update(request, link_id):
    mission = Mission.objects.get(id=link_id)
    form = MissionForm(instance=mission)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES, instance=mission)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'mission/mission_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def mission_delete(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')
    campaignID = mission.campaign.id

    if request.method == "POST":
        mission.delete()
        return HttpResponseRedirect('/airops/campaign/' + str(campaignID))

    context = {'item': mission, 'returnURL': returnURL}
    return render(request, 'mission/mission_delete.html', context=context)

# Package Views


@login_required(login_url='login')
@never_cache
def package(request, link_id):
    package = Package.objects.get(id=link_id)
    flights = package.flight_set.all()

    context = {'package_Object': package, 'flight_Object': flights}
    return render(request, 'package/package_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def package_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    form = PackageForm(initial={'mission': mission})
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'package/package_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def package_update(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    form = PackageForm(instance=package)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES, instance=package)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': missionID, 'returnURL': returnURL}
    return render(request, 'package/package_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def package_delete(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        package.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': package, 'returnURL': returnURL}
    return render(request, 'package/package_delete.html', context=context)


# Threat Views
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def threat_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')
    form = ThreatForm(initial={'mission': mission})

    if request.method == "POST":
        form = ThreatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'threat/threat_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def threat_update(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id
    form = ThreatForm(instance=threat)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = ThreatForm(request.POST, request.FILES, instance=threat)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'threat/threat_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def threat_delete(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id

    if request.method == "POST":
        threat.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': threat}
    return render(request, 'threat/threat_delete.html', context=context)

# Mission Imagery Views


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def mission_imagery_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = MissionImageryForm(initial={'mission': mission})

    if request.method == "POST":
        form = MissionImageryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'missionImagery/missionImagery_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def mission_imagery_update(request, link_id):
    imagery = MissionImagery.objects.get(id=link_id)

    missionID = imagery.mission.id
    form = MissionImageryForm(instance=imagery)

    if request.method == "POST":
        form = MissionImageryForm(
            request.POST, request.FILES, instance=imagery)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID}
    return render(request, 'missionImagery/missionImagery_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def mission_imagery_delete(request, link_id):
    imagery = MissionImagery.objects.get(id=link_id)
    missionID = imagery.mission.id
    if request.method == "POST":
        imagery.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': imagery}
    return render(request, 'missionImagery/missionImagery_delete.html', context=context)

### Flight Views ###


@login_required(login_url='login')
@never_cache
def flight(request, link_id):
    flight = Flight.objects.get(id=link_id)
    aircraft = flight.aircraft_set.all().order_by('-flight_lead')
    waypoints = flight.waypoint_set.all().order_by('number')
    targets = flight.targets.all()

    context = {'flight_Object': flight, 'aircraft_Object': aircraft,
               'waypoint_Object': waypoints, 'target_Object': targets}
    return render(request, 'flight/flight_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def flight_create(request, link_id):
    package = Package.objects.get(id=link_id)

    # Filter the target field to just targets from the mission.
    target = Target.objects.filter(mission=package.mission.id)

    form = FlightForm(target, initial={'package': package})

    if request.method == "POST":
        form = FlightForm(target, request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/package/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'flight/flight_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def flight_update(request, link_id):
    flight = Flight.objects.get(id=link_id)
    packageID = flight.package.id
    returnURL = request.GET.get('returnUrl')

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

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'flight/flight_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def flight_delete(request, link_id):
    flight = Flight.objects.get(id=link_id)
    packageID = flight.package.id
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        flight.delete()
        return HttpResponseRedirect('/airops/package/' + str(packageID))

    context = {'item': flight, 'returnURL': returnURL}
    return render(request, 'flight/flight_delete.html', context=context)

### Aircraft Views ###


@login_required(login_url='login')
def aircraft(request, link_id):

    aircraft = Aircraft.objects.get(id=link_id)

    context = {'aircraftObject': aircraft}
    return render(request, 'aircraft/aircraft_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def aircraft_create(request, link_id):
    flight = Flight.objects.get(id=link_id)

    # Filter the flights field to just targets from the mission.
    flights = Flight.objects.filter(package=flight.package.id)

    form = AircraftForm(
        flights, initial={'flight': flight})

    if request.method == "POST":
        form = AircraftForm(flights, request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/flight/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'aircraft/aircraft_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def aircraft_update(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id

    # Filter the flights field to just targets from the mission.
    flights = Flight.objects.filter(package=aircraft.flight.package.id)

    form = AircraftForm(flights, instance=aircraft)

    if request.method == "POST":
        form = AircraftForm(flights, request.POST,
                            request.FILES, instance=aircraft)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/flight/' + str(flightID))

    context = {'form': form, 'link': flightID}
    return render(request, 'aircraft/aircraft_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def aircraft_delete(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id

    if request.method == "POST":
        flight.delete()
        return HttpResponseRedirect('/airops/flight/' + str(flightID))

    context = {'item': aircraft}
    return render(request, 'aircraft/aircraft_delete.html', context=context)

### Target Views ###


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def target_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')
    form = TargetForm(initial={'mission': mission})

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'target/target_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def target_update(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id
    form = TargetForm(instance=target)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES, instance=target)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID, 'returnURL': returnURL}
    return render(request, 'target/target_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def target_delete(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        target.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': target}
    return render(request, 'target/target_delete.html', context=context)

### Support Views ###


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def support_create(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')
    form = SupportForm(initial={'mission': mission})

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'support/support_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def support_update(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = support.mission.id
    form = SupportForm(instance=support)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES, instance=support)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID, 'returnURL': returnURL}
    return render(request, 'support/support_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def support_delete(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        support.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': support}
    return render(request, 'support/support_delete.html', context=context)


# Waypoint Views
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def waypoint_create(request, link_id):
    flight = Flight.objects.get(id=link_id)

    form = WaypointForm(initial={'flight': flight})

    if request.method == "POST":
        form = WaypointForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/flight/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'waypoint/waypoint_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
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
            return HttpResponseRedirect('/airops/flight/' + str(flightID))

    context = {'form': form, 'link': flightID}
    return render(request, 'waypoint/waypoint_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'planner', 'player'])
def waypoint_delete(request, link_id):
    waypoint = Waypoint.objects.get(id=link_id)
    flightID = waypoint.flight.id

    if request.method == "POST":
        waypoint.delete()
        return HttpResponseRedirect('/airops/flight/' + str(flightID))

    context = {'item': waypoint}
    return render(request, 'waypoint/waypoint_delete.html', context=context)

# Other Views


def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)


@unauthenticated_user
def register_request(request):
    if request.user.is_authenticated:
        return redirect('campaign')
    else:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return HttpResponseRedirect('/airops/campaign')
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm
        return render(request=request, template_name="dashboard/register.html", context={"register_form": form})


@unauthenticated_user
@csrf_protect
def login_request(request):
    if request.user.is_authenticated:
        return redirect('campaign')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(
                        request, "You are now logged in as " + username + ".")
                    return redirect('campaign')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="dashboard/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return HttpResponseRedirect('/airops/campaign')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {
        'form': form
    })

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
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/
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
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    print("Path: " + path)
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # pdf = pisa.CreatePDF(html, dest=result, link_callback=fetch_resources)
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def download_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {'mission_object': mission, 'flight_object': flight}
    pdf = render_to_pdf('mission_card/pdf_template.html', data)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "missioncard.pdf"
    content = "attachment; filename=%s" % (filename)
    response['Content-Disposition'] = content
    return response


def view_mission_card(request, mission_id, flight_id):
    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)
    packages = mission.package_set.all()
    aircraft = flight.aircraft_set.all().order_by('-flight_lead')
    waypoints = flight.waypoint_set.all()
    supports = mission.support_set.all()
    targets = flight.targets.all()
    threats = mission.threat_set.all()
    #threat_details = threats.threat_name.harm_code

    data = {'mission_object': mission,
            'flight_object': flight, 'packages_object': packages, 'aircraft_object': aircraft, 'waypoints_object': waypoints, 'support_object': supports, 'target_object': targets, 'threat_object': threats}

    pdf = render_to_pdf('mission_card/pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def new_view_mission_card(request, mission_id, flight_id):

    mission = Mission.objects.get(id=mission_id)
    flight = Flight.objects.get(id=flight_id)

    data = {'mission_object': mission, 'flight_object': flight}

    template_path = 'mission_card/pdf_template.html'
    context = data
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mission_card.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=fetch_resources)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
