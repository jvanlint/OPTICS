from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

from ..models import Threat, Mission
from ..forms import ThreatForm

@login_required(login_url="account_login")
def threat_add_v2(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')

	form_title = 'Threat'

	form = ThreatForm(initial={'mission': mission})

	if request.method == "POST":
		form = ThreatForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def threat_update_v2(request, link_id):
	threat = Threat.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Threat'

	form = ThreatForm(instance=threat)

	if request.method == "POST":
		form = ThreatForm(request.POST, instance=threat)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def threat_delete_v2(request, link_id):
	threat = Threat.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	threat.delete()
	
	return HttpResponseRedirect(returnURL)