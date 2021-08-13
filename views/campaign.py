from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from django.views.decorators.cache import never_cache

from ..models import Campaign, UserProfile
from ..forms import CampaignForm

@login_required(login_url="account_login")
def campaign(request):
	
	order_by = request.GET.get("sort")
	if order_by:
		campaigns = Campaign.objects.order_by(order_by)
	else:
		campaigns = Campaign.objects.order_by('id')
	user_profile = UserProfile.objects.get(user=request.user)

	context = {
		"campaigns": campaigns, 
		'isAdmin': user_profile.is_admin(),
		}

	return render(request, "campaign/campaign.html", context=context)


@login_required(login_url="account_login")
def campaign_detail(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	missions = campaign.mission_set.all().order_by("number")
	user_profile = UserProfile.objects.get(user=request.user)
	campaign.refresh_from_db()

	context = {
		"campaign_Object": campaign,
		"mission_Object": missions,
		'isAdmin': user_profile.is_admin(),
		"user_timezone": request.user.profile.timezone,
	}

	return render(request, "campaign/campaign_detail.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def campaign_create(request):
	form = CampaignForm(initial={"creator": request.user.id})

	if request.method == "POST":
		form = CampaignForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, "Campaign successfully created.")
			return HttpResponseRedirect("/airops/campaign")

	context = {"form": form}
	return render(request, "campaign/campaign_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def campaign_update(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	form = CampaignForm(instance=campaign)
	returnURL = request.GET.get("returnUrl")

	if request.method == "POST":
		form = CampaignForm(request.POST, request.FILES, instance=campaign)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, "Campaign successfully updated.")
			return HttpResponseRedirect(returnURL)

	context = {"form": form, "link": link_id, "returnURL": returnURL}
	return render(request, "campaign/campaign_form.html", context=context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["admin", "planner", "player"])
def campaign_delete(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	returnURL = request.GET.get("returnUrl")

	if request.method == "POST":
		campaign.delete()
		messages.success(request, "Campaign successfully deleted.")
		return HttpResponseRedirect("/airops/campaign")

	context = {"item": campaign, "returnURL": returnURL}
	return render(request, "campaign/campaign_delete.html", context=context)