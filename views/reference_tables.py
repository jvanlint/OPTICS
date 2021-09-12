from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone

from django.urls import reverse

from ..models import  Terrain, Status, 
#  FlightTask, SupportType, WaypointType, ThreatType
#from .forms import FlightTaskForm, SupportTypeForm, TerrainForm, StatusForm, WaypointTypeForm, ThreatTypeForm

@login_required(login_url='login')
def reference_tables(request):
	terrain = Terrain.objects.order_by('name')
	status = Status.objects.order_by('name')
	waypoint_type = WaypointType.objects.order_by('name')
	flight_task = FlightTask.objects.order_by('name')
	support_type = SupportType.objects.order_by('name')
	threat_type = ThreatType.objects.order_by('name')
	breadcrumbs = {'Home': reverse('home'), 'Reference Tables':''}
	
	context = {'terrain_object': terrain, 
			   'status_object': status,
			   'waypoint_type_object': waypoint_type,
			   'flight_task_object': flight_task,
			   'support_type_object': support_type,
			   'threat_type_object': threat_type,
			   'breadcrumbs': breadcrumbs,
			   }
	# Render the HTML template index.html with the data in the context variable
	return render(request, 'v2/reference/reference_tables.html', context=context)

def evaluate_reference_object(table, link_id):
	if table == 'status':
		return Status
	elif table == 'terrain':
		return Terrain
	elif table == 'waypoint_type':
		return WaypointType
	elif table == 'flight_task':
		return FlightTask
	elif table == 'support_type':
		return SupportType
	elif table == 'threat_type':
		return ThreatType

def evaluate_reference_form(table):
	if table == 'status':
		return StatusForm
	elif table == 'terrain':
		return TerrainForm
	elif table == 'waypoint_type':
		return WaypointTypeForm
	elif table == 'flight_task':
		return FlightTaskForm
	elif table == 'support_type':
		return SupportTypeForm
	elif table == 'threat_type':
		return ThreatTypeForm