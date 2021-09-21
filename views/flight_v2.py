import os
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from ..models import Flight, FlightImagery, UserProfile, Comment, Package, Target
from ..forms import FlightForm, FlightImageryForm

@login_required(login_url="account_login")
def flight_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	aircraft = flight.aircraft_set.all()
	waypoints = flight.waypoint_set.all()
	targets = flight.targets.all()
	comments = flight.comments.all()
	imagery = flight.flightimagery_set.all()
	user_profile = UserProfile.objects.get(user=request.user)
	

	breadcrumbs = {'Home': reverse('campaigns'),  flight.package.mission.campaign.name: reverse('campaign_detail_v2', args=(flight.package.mission.campaign.id,)), flight.package.mission.name: reverse('mission_v2', args=(flight.package.mission.id,)), flight.package.name: reverse('package_v2', args=(flight.package.id,)), flight.callsign:''}

	context = {
		"flight_object": flight,
		"aircraft_object": aircraft,
		"waypoint_object": waypoints,
		"target_object": targets,
		"imagery_object": imagery,
		"isAdmin": user_profile.is_admin(),
		"comments": comments,
		"breadcrumbs": breadcrumbs,
	}

	return render(request, "v2/flight/flight.html", context=context)

@login_required(login_url="account_login")
def flight_add_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	
	# Filter the target field to just targets from the mission.
	target = Target.objects.filter(mission=package.mission.id)
	
	returnURL = request.GET.get('returnUrl')

	form_title = 'Flight'

	form = FlightForm(target, initial={'package': package})

	if request.method == "POST":
		form = FlightForm(target, request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.modified_by = request.user
			obj.created_by = request.user
			obj.save()
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def flight_update_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Flight'

	# Filter the target field to just targets from the mission.
	target = Target.objects.filter(mission=flight.package.mission.id)

	form = FlightForm(target, instance=flight)

	if request.method == "POST":
		form = FlightForm(target, request.POST, instance=flight)
		print(request.path)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.modified_by = request.user
			obj.save()
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)
	
@login_required(login_url="account_login")
def flight_delete_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	flight.delete()
	
	return HttpResponseRedirect(returnURL)

@login_required(login_url="account_login")
def flight_copy(request, link_id):
	flight = Flight.objects.get(id=link_id)
	packageID = flight.copy()

	return HttpResponseRedirect("/airops/package/" + str(packageID))
	
# ---------------- Flight Comments -------------------------
@login_required(login_url="account_login")
def flight_add_comment(request):
	# if this is a POST request we need to process the form data
	flight_id = request.GET.get("flight_id")
	returnURL = request.GET.get("returnUrl")

	if request.method == "POST":
		comment_data = request.POST.dict()
		comment = comment_data.get("comment_text")
		# Get the post object
		flight_object = Flight.objects.get(pk=flight_id)
		flight_object.comments.create(comment=comment, user=request.user)

	return HttpResponseRedirect(returnURL)

@login_required(login_url="account_login")
def flight_delete_comment(request, link_id):
	comment = Comment.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	
	comment.delete()
	
	return HttpResponseRedirect(returnURL)
	
# ---------------- Flight Imagery -------------------------
	
@login_required(login_url="account_login")
def flight_imagery_create_v2(request, link_id):
	flight = Flight.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")

	form = FlightImageryForm(initial={"flight": flight})
	form_title = "Flight Image"

	if request.method == "POST":
		form = FlightImageryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {
		"form": form,
		"form_title": form_title,
		"link": link_id,
		"returnURL": returnURL,
	}
	return render(request, 'v2/generic/data_entry_form.html', context=context)


@login_required(login_url="account_login")
def flight_imagery_update_v2(request, link_id):
	imagery = FlightImagery.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")

	form_title = "Flight Image"
	form = FlightImageryForm(instance=imagery)

	if request.method == "POST":
		form = FlightImageryForm(request.POST, request.FILES, instance=imagery)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {
		"form": form,
		"form_title": form_title,
		"link": link_id,
		"returnURL": returnURL,
	}
	return render(request, 'v2/generic/data_entry_form.html', context=context)


@login_required(login_url="account_login")
def flight_imagery_delete_v2(request, link_id):
	imagery = FlightImagery.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	
	# Check to see if an AO Image exists.
	if imagery:
		os.remove(os.path.join(settings.MEDIA_ROOT, str(imagery.image)))
		
	imagery.delete()
	return HttpResponseRedirect(returnURL)
