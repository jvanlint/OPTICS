from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

from ..models import Package, Mission, UserProfile
from ..forms import PackageForm

@login_required(login_url='login')
def package_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	flights = package.flight_set.all()
	user_profile = UserProfile.objects.get(user=request.user)
	
	breadcrumbs = {'Home': reverse('campaigns'),  package.mission.campaign.name: reverse('campaign_detail_v2', args=(package.mission.campaign.id,)), package.mission.name: reverse('mission_v2', args=(package.mission.id,)), package.name:''}
 
	context = {
			   'package_object': package,
			   'flight_object': flights,
			   "isAdmin": user_profile.is_admin(),
			   'breadcrumbs': breadcrumbs,
			   }

	return render(request, 
				  'v2/package/package.html', 
				  context=context)

@login_required(login_url='login')
def package_add_v2(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')

	form_title = 'Package'

	form = PackageForm(initial={'mission': mission})

	if request.method == "POST":
		form = PackageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def package_update_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Package'

	form = PackageForm(instance=package)

	if request.method == "POST":
		form = PackageForm(request.POST, instance=package)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)
	
@login_required(login_url='login')
def package_delete_v2(request, link_id):
	package = Package.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	package.delete()
	
	return HttpResponseRedirect(returnURL)