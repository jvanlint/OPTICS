from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse

from ..models import  Terrain, Status, Task, SupportType, WaypointType, ThreatType, Airframe
from ..forms import  TerrainForm, StatusForm, TaskForm, SupportTypeForm, WaypointTypeForm, ThreatTypeForm, AirframeForm

@login_required(login_url='login')
def reference_tables(request):
	terrain = Terrain.objects.order_by('name')
	status = Status.objects.order_by('name')
	waypoint_type = WaypointType.objects.order_by('name')
	flight_task = Task.objects.order_by('name')
	support_type = SupportType.objects.order_by('name')
	threat_type = ThreatType.objects.order_by('name')
	
	airframe = Airframe.objects.order_by('name')
	page=request.GET.get('page', 1)
	paginator = Paginator(airframe, 5)
	try:
		airframes = paginator.page(page)
	except PageNotAnInteger:
		airframes = paginator.page(1)
	except EmptyPage:
		airframes = paginator.page(paginator.num_pages)
	
	breadcrumbs = {'Home': reverse('home'), 'Reference Tables':''}
	
	context = {'terrain_object': terrain, 
			   'status_object': status,
			   'waypoint_type_object': waypoint_type,
			   'flight_task_object': flight_task,
			   'support_type_object': support_type,
			   'threat_type_object': threat_type,
			   'airframe_object': airframes,
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
		return Task
	elif table == 'support_type':
		return SupportType
	elif table == 'threat_type':
		return ThreatType
	elif table == 'airframe':
		return Airframe

def evaluate_reference_form(table):
	if table == 'status':
		return StatusForm
	elif table == 'terrain':
		return TerrainForm
	elif table == 'waypoint_type':
		return WaypointTypeForm
	elif table == 'flight_task':
		return TaskForm
	elif table == 'support_type':
		return SupportTypeForm
	elif table == 'threat_type':
		return ThreatTypeForm
	elif table == 'airframe':
		return AirframeForm

@login_required(login_url='login')
def reference_object_add(request, table):
	breadcrumbs = {'Home': reverse('home'), 'Reference Tables':reverse('reference_tables'), 'Add': ''}
	returnURL = request.GET.get('returnUrl')
	
	
	if request.method == 'POST':
		formobj = evaluate_reference_form(table)
		form = formobj(request.POST, 
					   request.FILES)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.date_modified = timezone.now()
			obj.user = request.user
			obj.save()
			#messages.success(request, "Campaign successfully created.")
			return redirect('reference_tables')
	else:
		form = evaluate_reference_form(table)

	context = {'form': form, 
			   'returnURL': returnURL,
			   'action': 'Add',
			   'breadcrumbs': breadcrumbs,
			   }

	# Render the HTML template index.html with the data in the context variable
	return render(request, 
				  'v2/generic/data_entry_form.html', 
				  context)
		
@login_required(login_url='login')
def reference_object_update(request, link_id, table):
	refobj = evaluate_reference_object(table, link_id)
	obj = refobj.objects.get(id=link_id)
	formobj = evaluate_reference_form(table)
	form = formobj(instance=obj)
	returnURL = request.GET.get('returnUrl')
	breadcrumbs = {'Home': reverse('home'), 'Reference Tables':reverse('reference_tables'), 'Edit': ''}
	
	if request.method == "POST":
		form = formobj(request.POST,
							instance=obj)
		if form.is_valid():
			form_obj=form.save(commit=False)
			form_obj.date_modified = timezone.now()
			form_obj.user = request.user
			form_obj.save()
			#messages.success(request, "Campaign successfully created.")
			return redirect('reference_tables')

	context = {'form': form, 
			   'action': 'Edit',
			   'returnURL': returnURL,
			   'breadcrumbs': breadcrumbs,
			   }
	return render(request, 
				  'v2/generic/data_entry_form.html', 
				  context=context)

@login_required(login_url='login')
def reference_object_delete(request, link_id, table):
	refobj = evaluate_reference_object(table, link_id)
	obj = refobj.objects.get(id=link_id)
	obj.delete()
	#messages.success(request, "Campaign successfully deleted.")
	return redirect('reference_tables')