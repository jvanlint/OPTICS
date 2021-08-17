from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Flight, FlightImagery, UserProfile
from ..forms import FlightImageryForm

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_imagery_create(request, link_id):
	flight = Flight.objects.get(id=link_id)

	form = FlightImageryForm(initial={"flight": flight})

	if request.method == "POST":
		form = FlightImageryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect("/airops/flight/" + str(link_id))

	context = {"form": form, "link": link_id}
	return render(request, "flightImagery/flightImagery_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_imagery_update(request, link_id):
	imagery = FlightImagery.objects.get(id=link_id)

	flightID = imagery.flight.id
	form = FlightImageryForm(instance=imagery)

	if request.method == "POST":
		form = FlightImageryForm(request.POST, request.FILES, instance=imagery)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			print("Form Saved!")
			return HttpResponseRedirect("/airops/flight/" + str(flightID))

	context = {"form": form, "link": flightID}
	return render(request, "flightImagery/flightImagery_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def flight_imagery_delete(request, link_id):
	imagery = FlightImagery.objects.get(id=link_id)
	flightID = imagery.flight.id
	if request.method == "POST":
		imagery.delete()
		return HttpResponseRedirect("/airops/flight/" + str(flightID))

	context = {"item": imagery}
	return render(request, "flightImagery/flightImagery_delete.html", context=context)