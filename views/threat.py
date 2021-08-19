from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Threat, Mission, UserProfile
from ..forms import ThreatForm

@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_create(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	form = ThreatForm(initial={"mission": mission})

	if request.method == "POST":
		form = ThreatForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect("/airops/mission/" + str(link_id))

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "threat/threat_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_update(request, link_id):
	threat = Threat.objects.get(id=link_id)
	missionID = threat.mission.id
	form = ThreatForm(instance=threat)
	returnURL = request.GET.get("returnUrl")

	if request.method == "POST":
		form = ThreatForm(request.POST, request.FILES, instance=threat)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			print("Form Saved!")
			return HttpResponseRedirect(returnURL)

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "threat/threat_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_delete(request, link_id):
	threat = Threat.objects.get(id=link_id)
	missionID = threat.mission.id

	if request.method == "POST":
		threat.delete()
		return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"item": threat}
	return render(request, "threat/threat_delete.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def threat_copy(request, link_id):
	threat = Threat.objects.get(id=link_id)
	missionID = threat.mission.id

	new_threat_instance = Threat(
		mission=threat.mission,
		threat_name=threat.threat_name + "(Copy)",
		name=threat.name,
		threat_type=threat.threat_type,
		description=threat.description,
	)
	new_threat_instance.save()

	return HttpResponseRedirect("/airops/mission/" + str(missionID))