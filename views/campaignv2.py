# For deleting physical files (like images) when campaign is deleted.
import os
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import User

from ..forms import CampaignForm
from ..models import Campaign, Comment, UserProfile


@login_required(login_url='login')
def campaigns_all(request):
	"""
	Retrieves all campaign objects and returns a HTML file displaying all objects.
	
	Args:
		request: The Django request object.
	
	Returns:
		A rendered HTML page with context containing campaign data, whether the user is an admin and breadcrumbs.
	"""
	
	campaigns_queryset = Campaign.objects.order_by('id')
	user_profile = UserProfile.objects.get(user=request.user)
	
	breadcrumbs = {'Home': ''}
	
	context = {'campaigns': campaigns_queryset, 
			   'isAdmin': user_profile.is_admin(),
			   'breadcrumbs': breadcrumbs,
			   }
	

	# Render the HTML template with the data in the context variable
	return render(request, 
		'v2/campaign/campaigns.html', 
		context=context
	)
	
@login_required(login_url='login')
def campaign_detail_v2(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	missions = campaign.mission_set.all().order_by('number')
	comments = campaign.comments.all()
	user_profile = UserProfile.objects.get(user=request.user)
	
	breadcrumbs = {'Home': reverse_lazy('campaigns'),  campaign.name: ''}

	campaign.refresh_from_db()

	context = {'campaign_object': campaign, 
			   'mission_object': missions, 
			   'isAdmin': user_profile.is_admin(), 
			   'comments': comments,
			   'breadcrumbs': breadcrumbs,
			   }

	return render(request, 
				  'v2/campaign/campaign.html', 
				  context=context)
	
@login_required(login_url='login')
def campaign_add_v2(request):
	
	breadcrumbs = {'Home': reverse('home'), 'Add': ''}
	
	if request.method == 'POST':
		form = CampaignForm(request.POST, 
							request.FILES)
		if form.is_valid():
			form.save(commit=True)
			#messages.success(request, "Campaign successfully created.")
			return HttpResponseRedirect(reverse_lazy('campaigns'))
	else:
		form = CampaignForm(initial={'creator': request.user.id})

	context = {'form': form, 
			   'action': 'Add',
			   'breadcrumbs': breadcrumbs,
			   }

	# Render the HTML template index.html with the data in the context variable
	return render(request, 
				  'v2/campaign/campaign_form.html', 
				  context)

@login_required(login_url='login')
def campaign_update_v2(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	form = CampaignForm(instance=campaign)
	returnURL = request.GET.get('returnUrl')
	breadcrumbs = {'Home': reverse_lazy('campaigns'),  campaign.name: reverse_lazy('campaign_detail_v2', args=(campaign.id,)), 'Edit': ''}

	if request.method == "POST":
		form = CampaignForm(request.POST, 
							request.FILES, 
							instance=campaign)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			#messages.success(request, "Campaign successfully updated.")
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 
			   'link': link_id,
			   'returnURL': returnURL,
			   'breadcrumbs': breadcrumbs,
			   'action': 'Edit'}
	return render(request, 
				  'v2/campaign/campaign_form.html', 
				  context=context)

@login_required(login_url='login')
def campaign_delete_v2(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	

	# Delete the campaign thumbnail before deleting the actual DB record.
	#Check to see if a campaign thumbnail exists.
	if campaign.campaignImage:
		os.remove(os.path.join(settings.MEDIA_ROOT,  str(campaign.campaignImage)))
		
	#Check to see if an AO Image exists.
	if campaign.aoImage:
		os.remove(os.path.join(settings.MEDIA_ROOT,  str(campaign.aoImage)))
	
	campaign.delete()
	#messages.success(request, "Campaign successfully deleted.")
	return HttpResponseRedirect(returnURL)
	
# **** End Campaigns Code *****