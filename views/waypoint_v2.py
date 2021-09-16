import os
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from ..models import Flight, Waypoint
from ..forms import WaypointForm

@login_required(login_url='login')
def waypoint_add_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')

	form_title = 'Waypoint'

	form = WaypointForm(initial={"flight": flight})

	if request.method == "POST":
		form = WaypointForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def waypoint_update_v2(request, link_id):
	waypoint = Waypoint.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Waypoint'

	form = WaypointForm(instance=waypoint)

	if request.method == "POST":
		form = WaypointForm(request.POST, instance=waypoint)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def waypoint_delete_v2(request, link_id):
	waypoint = Waypoint.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	waypoint.delete()
	
	return HttpResponseRedirect(returnURL)
	
@login_required(login_url="login")
def waypoint_copy_v2(request, link_id):
	waypoint = Waypoint.objects.get(id=link_id)
	flightID = waypoint.copy()

	returnURL = request.GET.get("returnUrl")

	return HttpResponseRedirect(returnURL)