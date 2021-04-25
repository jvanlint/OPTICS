from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode

from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_protect

from .models import Campaign, Mission, Package, Flight, Threat, Aircraft, Target, Support, Waypoint
from .forms import CampaignForm, MissionForm, NewUserForm, PackageForm, ThreatForm, FlightForm, AircraftForm, TargetForm, SupportForm, WaypointForm
# For PDF
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from io import BytesIO


class CampaignView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')


class MyFormView(View):
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})
