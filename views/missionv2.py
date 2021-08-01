import os
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from ..models import Campaign, Mission, UserProfile, MissionFile
from ..forms import MissionForm


# ---------------- Mission -------------------------

@login_required(login_url='login')
def mission(request, link_id):
	mission_queryset = Mission.objects.get(id=link_id)
	mission_files_queryset = mission_queryset.missionfile_set.all()
	combat_files_queryset = mission_queryset.combatflitefile_set.all()
	comments = mission_queryset.comments.all()
	user_profile = UserProfile.objects.get(user=request.user)
	
	breadcrumbs = {'Home': reverse('home'),  mission_queryset.campaign.campaign_name: reverse('campaign_detail', args=(mission_queryset.campaign.id,)), mission_queryset.name:''}
 
	context = {
			   'mission_object': mission_queryset, 
			   'mission_files': mission_files_queryset,
			   'combat_files': combat_files_queryset,
			   'isAdmin': user_profile.is_admin(), 
			   'comments': comments,
			   'breadcrumbs': breadcrumbs,
			   }

	return render(request, 
				  'mission/mission.html', 
				  context=context)

@login_required(login_url='login')
def mission_add(request, link_id):
	campaign = Campaign.objects.get(id=link_id)
	missionCount = campaign.mission_set.count() + 1
	returnURL = request.GET.get('returnUrl')

	form_title = 'Mission'

	form = MissionForm(initial={'campaign': campaign, 'number': missionCount, 'creator': request.user.id})

	if request.method == "POST":
		form = MissionForm(request.POST, request.FILES)
		if form.is_valid():
			tmp = form.save(commit=False)
			tmp.creator = request.user
			tmp.save()
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'generic/data_entry_form.html', context=context)


@login_required(login_url='login')
def mission_update(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	image_url = request.build_absolute_uri(mission.campaign.thumbnail_image.url)
	
	mission.create_discord_event(image_url)
	
	

	form_title = 'Mission'

	form = MissionForm(instance=mission)

	if request.method == "POST":
		form = MissionForm(request.POST, request.FILES, instance=mission)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def mission_delete(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	mission_files = mission.missionfile_set.all()
	
	#Check to see if an AO Image exists.
	if mission_files:
		for file in mission_files:
			os.remove(os.path.join(settings.MEDIA_ROOT,  str(file.mission_file)))
	
	mission.delete()
	
	return HttpResponseRedirect(returnURL)

def mission_add_comment(request):
	# if this is a POST request we need to process the form data
	mission_id = request.GET.get('mission_id')
	returnURL = request.GET.get('returnUrl')

	if request.method == 'POST':
		comment_data = request.POST.dict()
		comment = comment_data.get("comment_text")
		# Get the post object
		mission_object = Mission.objects.get(pk=mission_id)
		mission_object.comments.create(comment=comment, 
								 user=request.user)
		
	return HttpResponseRedirect(returnURL)

@login_required(login_url='login')
def mission_file_delete(request, link_id):
	mission_file_obj = MissionFile.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	
	#Check to see if an AO Image exists.
	if mission_file_obj:
		os.remove(os.path.join(settings.MEDIA_ROOT,  str(mission_file_obj.mission_file)))
	
	mission_file_obj.delete()
	
	return HttpResponseRedirect(returnURL)