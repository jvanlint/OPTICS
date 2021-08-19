from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Support, Mission, UserProfile
from ..forms import SupportForm

@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_create(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	form = SupportForm(initial={"mission": mission})

	if request.method == "POST":
		form = SupportForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect("/airops/mission/" + str(link_id))

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "support/support_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_update(request, link_id):
	support = Support.objects.get(id=link_id)
	missionID = support.mission.id
	form = SupportForm(instance=support)
	returnURL = request.GET.get("returnUrl")

	if request.method == "POST":
		form = SupportForm(request.POST, request.FILES, instance=support)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			print("Form Saved!")
			return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"form": form, "link": missionID, "returnURL": returnURL}
	return render(request, "support/support_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_delete(request, link_id):
	support = Support.objects.get(id=link_id)
	missionID = support.mission.id

	if request.method == "POST":
		support.delete()
		return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"item": support}
	return render(request, "support/support_delete.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def support_copy(request, link_id):
	support = Support.objects.get(id=link_id)
	missionID = support.mission.id

	new_support_instance = Support(
		mission=support.mission,
		callsign=support.callsign + "(Copy)",
		support_type=support.support_type,
		player_name=support.player_name,
		frequency=support.frequency,
		tacan=support.tacan,
		altitude=support.altitude,
		speed=support.speed,
		brc=support.brc,
		icls=support.icls,
		notes=support.notes,
	)
	new_support_instance.save()

	return HttpResponseRedirect("/airops/mission/" + str(missionID))