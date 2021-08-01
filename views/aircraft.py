from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Aircraft, UserProfile
from ..forms import AircraftForm

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