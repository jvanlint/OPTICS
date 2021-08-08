from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Flight, Package, Target, UserProfile
from ..forms import FlightForm

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
	
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_copy(request, link_id):
	flight = Flight.objects.get(id=link_id)
	packageID = flight.copy()

	return HttpResponseRedirect("/airops/package/" + str(packageID))
