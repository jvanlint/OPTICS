from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Waypoint, Flight, UserProfile
from ..forms import WaypointForm

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
	
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def waypoint_copy(request, link_id):
	waypoint = Waypoint.objects.get(id=link_id)
	flightID = waypoint.copy()

	return HttpResponseRedirect("/airops/flight/" + str(flightID))