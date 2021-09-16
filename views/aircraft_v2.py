import os
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from ..models import Flight, Aircraft
from ..forms import AircraftForm

@login_required(login_url='login')
def aircraft_add_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	# Filter the flights field to just targets from the mission.
	flights = Flight.objects.filter(package=flight.package.id)

	form_title = 'Aircraft'

	form = AircraftForm(flights, initial={"flight": flight})

	if request.method == "POST":
		form = AircraftForm(flights, request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def aircraft_update_v2(request, link_id):
	aircraft = Aircraft.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	# Filter the flights field to just targets from the mission.
	flights = Flight.objects.filter(package=aircraft.flight.package.id)
	
	form_title = 'Aircraft'

	form = AircraftForm(flights, instance=aircraft)

	if request.method == "POST":
		form = AircraftForm(flights, request.POST, instance=aircraft)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def aircraft_delete_v2(request, link_id):
	aircraft = Aircraft.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	aircraft.delete()
	
	return HttpResponseRedirect(returnURL)
	
@login_required(login_url="login")
def aircraft_copy_v2(request, link_id):
	aircraft = Aircraft.objects.get(id=link_id)
	flightID = aircraft.copy()

	returnURL = request.GET.get("returnUrl")

	return HttpResponseRedirect(returnURL)