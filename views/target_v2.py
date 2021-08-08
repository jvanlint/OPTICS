from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

from ..models import Target, Mission
from ..forms import TargetForm

@login_required(login_url='login')
def target_add_v2(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')

	form_title = 'Target'

	form = TargetForm(initial={'mission': mission})

	if request.method == "POST":
		form = TargetForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def target_update_v2(request, link_id):
	target = Target.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Target'

	form = TargetForm(instance=target)

	if request.method == "POST":
		form = TargetForm(request.POST, instance=target)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url='login')
def target_delete_v2(request, link_id):
	target = Target.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	target.delete()
	
	return HttpResponseRedirect(returnURL)