from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode

from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_protect

from .models import Campaign, Mission, Package, Flight, Threat, Aircraft, Target, Support
from .forms import CampaignForm, MissionForm, NewUserForm, PackageForm, ThreatForm, FlightForm, AircraftForm, TargetForm, SupportForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_campaigns = Campaign.objects.all().count()
    #num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_missions = Mission.objects.count()

    context = {
        'num_campaigns': num_campaigns,
        'num_missions': num_missions,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Campaign Views

def campaign(request):
    campaigns = Campaign.objects.order_by('id')

    context = {'campaigns': campaigns}

    return render(request, 'campaign/campaign.html', context=context)


def campaign_detail(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missions = campaign.mission_set.all().order_by('number')

    campaign.refresh_from_db()

    context = {'campaign': campaign, 'missions': missions}

    return render(request, 'campaign/campaign_detail.html', context=context)


def campaign_create(request):
    form = CampaignForm()

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully created.")
            return HttpResponseRedirect('/airops/campaign')

    context = {'form': form}
    return render(request, 'campaign/campaign_form.html', context=context)


def campaign_update(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    form = CampaignForm(instance=campaign)

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully updated.")
            return HttpResponseRedirect('/airops/campaign/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'campaign/campaign_form.html', context=context)


def campaign_delete(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    if request.method == "POST":
        campaign.delete()
        messages.success(request, "Campaign successfully deleted.")
        return HttpResponseRedirect('/airops/campaign')

    context = {'item': campaign}
    return render(request, 'campaign/campaign_delete.html', context=context)

# Mission Views


@never_cache
def mission(request, link_id):
    mission = Mission.objects.get(id=link_id)
    packages = mission.package_set.all()
    threat = mission.threat_set.all()
    target = mission.target_set.all()
    support = mission.support_set.all()

    context = {'mission_object': mission,
               'package_object': packages, 'threat_object': threat, 'target_object': target, 'support_object': support}
    return render(request, 'mission/mission_detail.html', context)


def mission_create(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missionCount = campaign.mission_set.count() + 1
    form = MissionForm(initial={'campaign': campaign, 'number': missionCount})
    #form.base_fields['number'].initial = missionCount

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/campaign/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'mission/mission_form.html', context=context)


def mission_update(request, link_id):
    mission = Mission.objects.get(id=link_id)
    form = MissionForm(instance=mission)

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES, instance=mission)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'mission/mission_form.html', context=context)


def mission_delete(request, link_id):
    mission = Mission.objects.get(id=link_id)
    if request.method == "POST":
        mission.delete()
        return HttpResponseRedirect('/airops/campaign')

    context = {'item': mission}
    return render(request, 'mission/mission_delete.html', context=context)

# Package Views


@never_cache
def package(request, link_id):
    package = Package.objects.get(id=link_id)
    flights = package.flight_set.all()

    context = {'packageObject': package, 'flightObject': flights}
    return render(request, 'package/package_detail.html', context)


def package_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = PackageForm(initial={'mission': mission})

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'package/package_form.html', context=context)


def package_update(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    form = PackageForm(instance=package)

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES, instance=package)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID}
    return render(request, 'package/package_form.html', context=context)


def package_delete(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    if request.method == "POST":
        package.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': package}
    return render(request, 'package/package_delete.html', context=context)


# Threat Views
def threat_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = ThreatForm(initial={'mission': mission})

    if request.method == "POST":
        form = ThreatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'threat/threat_form.html', context=context)


def threat_update(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id
    form = ThreatForm(instance=threat)

    if request.method == "POST":
        form = ThreatForm(request.POST, request.FILES, instance=threat)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': link_id}
    return render(request, 'threat/threat_form.html', context=context)


def threat_delete(request, link_id):
    threat = Threat.objects.get(id=link_id)
    missionID = threat.mission.id
    if request.method == "POST":
        threat.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': threat}
    return render(request, 'threat/threat_delete.html', context=context)

### Flight Views ###


@never_cache
def flight(request, link_id):
    flight = Flight.objects.get(id=link_id)
    aircraft = flight.aircraft_set.all()

    context = {'flightObject': flight, 'aircraftObject': aircraft}
    return render(request, 'flight/flight_detail.html', context)


def flight_create(request, link_id):
    package = Package.objects.get(id=link_id)
    target = Target.objects.filter(mission=package.mission.id)
    print(target)
    form = FlightForm(target, initial={'package': package})

    if request.method == "POST":
        form = FlightForm(1, request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/package/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'flight/flight_form.html', context=context)


def flight_update(request, link_id):
    flight = Flight.objects.get(id=link_id)
    packageID = flight.package.id
    form = FlightForm(instance=flight)

    if request.method == "POST":
        form = FlightForm(request.POST, request.FILES, instance=flight)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/flight/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'flight/flight_form.html', context=context)


def flight_delete(request, link_id):
    flight = Flight.objects.get(id=link_id)
    packageID = flight.package.id
    if request.method == "POST":
        flight.delete()
        return HttpResponseRedirect('/airops/package/' + str(packageID))

    context = {'item': flight}
    return render(request, 'flight/flight_delete.html', context=context)

### Aircraft Views ###


def aircraft(request, link_id):

    aircraft = Aircraft.objects.get(id=link_id)

    context = {'aircraftObject': aircraft}
    return render(request, 'aircraft/aircraft_detail.html', context)


def aircraft_create(request, link_id):
    flight = Flight.objects.get(id=link_id)

    form = AircraftForm(initial={'flight': flight})

    if request.method == "POST":
        form = AircraftForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/flight/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'aircraft/aircraft_form.html', context=context)


def aircraft_update(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id
    form = AircraftForm(instance=aircraft)

    if request.method == "POST":
        form = AircraftForm(request.POST, request.FILES, instance=aircraft)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/aircraft/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'aircraft/aircraft_form.html', context=context)


def aircraft_delete(request, link_id):
    aircraft = Aircraft.objects.get(id=link_id)
    flightID = aircraft.flight.id

    if request.method == "POST":
        flight.delete()
        return HttpResponseRedirect('/airops/flight/' + str(flightID))

    context = {'item': aircraft}
    return render(request, 'aircraft/aircraft_delete.html', context=context)

### Target Views ###


def target_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = TargetForm(initial={'mission': mission})

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'target/target_form.html', context=context)


def target_update(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id
    form = TargetForm(instance=target)

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES, instance=target)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID}
    return render(request, 'target/target_form.html', context=context)


def target_delete(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        target.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': target}
    return render(request, 'target/target_delete.html', context=context)

### Support Views ###


def support_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = SupportForm(initial={'mission': mission})

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'support/support_form.html', context=context)


def support_update(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = support.mission.id
    form = SupportForm(instance=support)

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES, instance=support)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID}
    return render(request, 'support/support_form.html', context=context)


def support_delete(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        support.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': support}
    return render(request, 'support/support_delete.html', context=context)

# Other Views


def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)


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
