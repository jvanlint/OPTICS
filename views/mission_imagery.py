from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Mission, MissionImagery, UserProfile
from ..forms import MissionImageryForm

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_imagery_create(request, link_id):
	mission = Mission.objects.get(id=link_id)

	form = MissionImageryForm(initial={"mission": mission})

	if request.method == "POST":
		form = MissionImageryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect("/airops/mission/" + str(link_id))

	context = {"form": form, "link": link_id}
	return render(request, "missionImagery/missionImagery_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_imagery_update(request, link_id):
	imagery = MissionImagery.objects.get(id=link_id)

	missionID = imagery.mission.id
	form = MissionImageryForm(instance=imagery)

	if request.method == "POST":
		form = MissionImageryForm(request.POST, request.FILES, instance=imagery)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			print("Form Saved!")
			return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"form": form, "link": missionID}
	return render(request, "missionImagery/missionImagery_form.html", context=context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def mission_imagery_delete(request, link_id):
	imagery = MissionImagery.objects.get(id=link_id)
	missionID = imagery.mission.id
	if request.method == "POST":
		imagery.delete()
		return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"item": imagery}
	return render(request, "missionImagery/missionImagery_delete.html", context=context)