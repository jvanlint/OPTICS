from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Target, Mission, UserProfile
from ..forms import TargetForm

@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_create(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")
	form = TargetForm(initial={"mission": mission})

	if request.method == "POST":
		form = TargetForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect("/airops/mission/" + str(link_id))

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "target/target_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_update(request, link_id):
	target = Target.objects.get(id=link_id)
	missionID = target.mission.id
	form = TargetForm(instance=target)
	returnURL = request.GET.get("returnUrl")

	if request.method == "POST":
		form = TargetForm(request.POST, request.FILES, instance=target)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			print("Form Saved!")
			return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"form": form, "link": missionID, "returnURL": returnURL}
	return render(request, "target/target_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_delete(request, link_id):
	target = Target.objects.get(id=link_id)
	missionID = target.mission.id

	if request.method == "POST":
		target.delete()
		return HttpResponseRedirect("/airops/mission/" + str(missionID))

	context = {"item": target}
	return render(request, "target/target_delete.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def target_copy(request, link_id):
	target = Target.objects.get(id=link_id)
	missionID = target.mission.id

	new_target_instance = Target(
		mission=target.mission,
		name=target.name + "(Copy)",
		lat=target.lat,
		long=target.long,
		elev=target.elev,
		notes=target.notes,
	)
	new_target_instance.save()

	return HttpResponseRedirect("/airops/mission/" + str(missionID))