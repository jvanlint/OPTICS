from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache
from django.core import serializers

from ..models import Mission, Package, Campaign, Aircraft, UserProfile
from ..forms import MissionForm

@login_required(login_url="account_login")
@never_cache
def mission(request, link_id):
	mission = Mission.objects.get(id=link_id)
	packages = mission.package_set.all()
	threat = mission.threat_set.all()
	target = mission.target_set.all()
	support = mission.support_set.all()
	imagery = mission.missionimagery_set.all()
	user_profile = UserProfile.objects.get(user=request.user)

	context = {
		"mission_object": mission,
		"package_object": packages,
		"threat_object": threat,
		"target_object": target,
		"support_object": support,
		"imagery_object": imagery,
		'isAdmin': user_profile.is_admin(),
		"isPlanner": user_profile.is_planner(),
		"user_timezone": request.user.profile.timezone,
	}
	return render(request, "mission/mission_detail.html", context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_create(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	missionCount = campaign.mission_set.count() + 1
	returnURL = request.GET.get("returnUrl")
	image_url = request.build_absolute_uri(campaign.campaignImage.url)

	form = MissionForm(initial={"campaign": campaign, "number": missionCount})
	# form.base_fields['number'].initial = missionCount

	if request.method == "POST":
		form = MissionForm(request.POST, request.FILES)
		if form.is_valid():
			# Mission date and time are combined in the form's clean function
			# https://stackoverflow.com/questions/53742129/how-do-you-modify-form-data-before-saving-it-while-using-djangos-createview

			# form.mission_date=form.mission_date.replace(tzinfo=timezone.utc)
			'''
			combine the time and date responses and create a date/time to be 
			saved in the mission datetime field.
			Do this also for the update view below (extract to a function)
			Also will need to do the reverse for the view of this field.
			https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
			https://www.programiz.com/python-programming/datetime
			https://realpython.com/python39-new-features/#proper-time-zone-support
			check settings.py for correct time format
			https://docs.djangoproject.com/en/3.2/ref/settings/#time-input-formats
			https://docs.djangoproject.com/en/3.2/ref/models/fields/#datetimefield
			http://diveintohtml5.info/forms.html
			mission_data is datetime UTC+10 (settings.py default timezone)
			mission_time is string
			mission_game_time is string
			mission_game_date is datetime UTC+10
			'''
			
			
			mission = form.save(commit=True)
			if mission.notify_discord:
				mission.create_discord_event(image_url, request)
			return HttpResponseRedirect("/airops/campaign/" + str(link_id))

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "mission/mission_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_update(request, link_id):
	mission = Mission.objects.get(id=link_id)
	form = MissionForm(instance=mission)
	returnURL = request.GET.get("returnUrl")
	
	image_url = request.build_absolute_uri(mission.campaign.campaignImage.url)
	
	if request.method == "POST":
		form = MissionForm(request.POST, request.FILES, instance=mission)
		
		if form.is_valid():
			saved_obj = form.save(commit=True)
			# If flag is enabled Post to Discord.
			if saved_obj.notify_discord:
				mission.create_discord_event(image_url, request)
			return HttpResponseRedirect(returnURL)

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "mission/mission_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_delete(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	campaignID = mission.campaign.id

	if request.method == "POST":
		if mission.discord_msg_id:
			mission.delete_discord_event()
		mission.delete()
		return HttpResponseRedirect("/airops/campaign/" + str(campaignID))

	context = {"item": mission, "returnURL": returnURL}
	return render(request, "mission/mission_delete.html", context=context)

@login_required(login_url="account_login")
def mission_signup(request, link_id):  # link_id is the mission ID
	mission = Mission.objects.get(id=link_id)
	packages = mission.package_set.all()

	has_seat = 0
	package_list = serializers.serialize("python", packages)
	for package in package_list:
		has_seat += (
			Aircraft.objects.filter(flight__package__id=package["pk"])
			.filter(pilot=request.user)
			.count()
		)
		has_seat += (
			Aircraft.objects.filter(flight__package__id=package["pk"])
			.filter(rio_wso=request.user)
			.count()
		)
	campaign = Campaign.objects.get(mission=mission)
	is_owner = campaign.creator == request.user
	context = {
		"mission_object": mission,
		"package_object": packages,
		"has_seat": has_seat,
		"is_owner": is_owner,
	}

	return render(request, "mission/mission_signup.html", context)
	
@login_required(login_url="account_login")
def mission_signup_update(request, link_id, seat_id):
	returnURL = request.GET.get("returnUrl")
	aircraft = Aircraft.objects.get(pk=link_id)
	if seat_id == 1:
		aircraft.pilot = request.user
	else:
		aircraft.rio_wso = request.user

	aircraft.save()

	return HttpResponseRedirect(returnURL)


@login_required(login_url="account_login")
def mission_signup_remove(request, link_id, seat_id):
	returnURL = request.GET.get("returnUrl")
	aircraft = Aircraft.objects.get(pk=link_id)
	if seat_id == 1:
		aircraft.pilot = None
	else:
		aircraft.rio_wso = None

	aircraft.save()

	return HttpResponseRedirect(returnURL)
	
@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_copy(request, link_id):
	mission = Mission.objects.get(id=link_id)
	campaignID = mission.copy()

	return HttpResponseRedirect("/airops/campaign/" + str(campaignID))