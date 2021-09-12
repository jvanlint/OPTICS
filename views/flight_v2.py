import os
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from ..models import Flight, FlightImagery, UserProfile, Comment
from ..forms import FlightForm, FlightImageryForm

@login_required(login_url="account_login")
def flight_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	aircraft = flight.aircraft_set.all()
	comments = flight.comments.all()
	imagery = flight.flightimagery_set.all()
	user_profile = UserProfile.objects.get(user=request.user)
	

	breadcrumbs = {'Home': reverse('campaigns'),  flight.package.mission.campaign.name: reverse('campaign_detail_v2', args=(flight.package.mission.campaign.id,)), flight.package.mission.name: reverse('mission_v2', args=(flight.package.mission.id,)), flight.package.name: reverse('package_v2', args=(flight.package.id,)), flight.callsign:''}

	context = {
		"flight_object": flight,
		"aircraft_object": aircraft,
		"imagery_object": imagery,
		"isAdmin": user_profile.is_admin(),
		"comments": comments,
		"breadcrumbs": breadcrumbs,
	}

	return render(request, "v2/flight/flight.html", context=context)