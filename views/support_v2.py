from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

from ..models import Support, Mission
from ..forms import SupportForm

@login_required(login_url="account_login")
def support_add_v2(request, link_id):
	mission = Mission.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')

	form_title = 'Support'

	form = SupportForm(initial={'mission': mission})

	if request.method == "POST":
		form = SupportForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def support_update_v2(request, link_id):
	support = Support.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	form_title = 'Support'

	form = SupportForm(instance=support)

	if request.method == "POST":
		form = SupportForm(request.POST, instance=support)
		print(request.path)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(returnURL)

	context = {'form': form, 'form_title': form_title,
			   'link': link_id, 'returnURL': returnURL}
	return render(request, 'v2/generic/data_entry_form.html', context=context)

@login_required(login_url="account_login")
def support_delete_v2(request, link_id):
	support = Support.objects.get(id=link_id)
	returnURL = request.GET.get('returnUrl')
	
	support.delete()
	
	return HttpResponseRedirect(returnURL)