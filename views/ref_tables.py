from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse

from ..models import (
    Terrain,
    Status,
    Task,
    SupportType,
    WaypointType,
    ThreatType,
    Airframe,
)
from ..forms import (
    TerrainForm,
    StatusForm,
    TaskForm,
    SupportTypeForm,
    WaypointTypeForm,
    ThreatTypeForm,
    AirframeForm,
)


@login_required(login_url="account_login")
def reference_tables(request):

    airframe = Airframe.objects.order_by("name")  # Always update the airframe context
    terrain = Terrain.objects.order_by("name")
    status = Status.objects.order_by("name")
    waypoint_type = WaypointType.objects.order_by("name")
    flight_task = Task.objects.order_by("name")
    support_type = SupportType.objects.order_by("name")
    threat_type = ThreatType.objects.order_by("name")

    page_num = request.GET.get("page", 1)
    waypoint_paginated = Paginator(object_list=waypoint_type, per_page=5).get_page(
        page_num
    )
    airframe_paginated = Paginator(object_list=airframe, per_page=5).get_page(page_num)
    flight_task_paginated = Paginator(object_list=flight_task, per_page=5).get_page(
        page_num
    )
    campaign_status_paginated = Paginator(object_list=status, per_page=5).get_page(
        page_num
    )
    terrain_paginated = Paginator(object_list=terrain, per_page=5).get_page(page_num)
    support_type_paginated = Paginator(object_list=support_type, per_page=5).get_page(
        page_num
    )
    threat_type_paginated = Paginator(object_list=threat_type, per_page=5).get_page(
        page_num
    )

    breadcrumbs = {"Home": reverse("index"), "Reference Tables": ""}

    template = "v2/reference/reference_tables.html"
    context = {
        "terrain_object": terrain_paginated,
        "status_object": campaign_status_paginated,
        "waypoint_type_object": waypoint_paginated,
        "flight_task_object": flight_task_paginated,
        "support_type_object": support_type_paginated,
        "threat_type_object": threat_type_paginated,
        "airframe_object": airframe_paginated,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, template_name=template, context=context)


def waypoint_type_page_manager(request):
    waypoint_type = WaypointType.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    waypoint_paginated = Paginator(object_list=waypoint_type, per_page=5).get_page(
        page_num
    )

    template = "v2/reference/includes/waypoint_types.html"
    context = {"waypoint_type_object": waypoint_paginated}

    return render(request, template_name=template, context=context)


def airframe_page_manager(request):
    airframe = Airframe.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    airframe_paginated = Paginator(object_list=airframe, per_page=5).get_page(page_num)

    template = "v2/reference/includes/airframes.html"
    context = {"airframe_object": airframe_paginated}

    return render(request, template_name=template, context=context)


def flight_task_page_manager(request):
    flight_task = Task.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    flight_task_paginated = Paginator(object_list=flight_task, per_page=5).get_page(
        page_num
    )

    template = "v2/reference/includes/flight_tasks.html"
    context = {"flight_task_object": flight_task_paginated}

    return render(request, template_name=template, context=context)


def campaign_status_page_manager(request):
    campaign_status = Status.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    campaign_status_paginated = Paginator(
        object_list=campaign_status, per_page=5
    ).get_page(page_num)

    template = "v2/reference/includes/campaign_status.html"
    context = {"status_object": campaign_status_paginated}

    return render(request, template_name=template, context=context)


def terrain_page_manager(request):
    terrain = Terrain.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    terrain_paginated = Paginator(object_list=terrain, per_page=5).get_page(page_num)

    template = "v2/reference/includes/terrain.html"
    context = {"terrain_object": terrain_paginated}

    return render(request, template_name=template, context=context)


def support_type_page_manager(request):
    support_type = SupportType.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    support_type_paginated = Paginator(object_list=support_type, per_page=5).get_page(
        page_num
    )

    template = "v2/reference/includes/support_types.html"
    context = {"support_type_object": support_type_paginated}

    return render(request, template_name=template, context=context)


def threat_type_page_manager(request):
    threat_type = ThreatType.objects.order_by("name")
    page_num = request.GET.get("page", 1)
    threat_type_paginated = Paginator(object_list=threat_type, per_page=5).get_page(
        page_num
    )

    template = "v2/reference/includes/threat_types.html"
    context = {"threat_type_object": threat_type_paginated}

    return render(request, template_name=template, context=context)


def evaluate_reference_object(table, link_id):
    if table == "status":
        return Status
    elif table == "terrain":
        return Terrain
    elif table == "waypoint_type":
        return WaypointType
    elif table == "flight_task":
        return Task
    elif table == "support_type":
        return SupportType
    elif table == "threat_type":
        return ThreatType
    elif table == "airframe":
        return Airframe


def evaluate_reference_form(table):
    if table == "status":
        return StatusForm
    elif table == "terrain":
        return TerrainForm
    elif table == "waypoint_type":
        return WaypointTypeForm
    elif table == "flight_task":
        return TaskForm
    elif table == "support_type":
        return SupportTypeForm
    elif table == "threat_type":
        return ThreatTypeForm
    elif table == "airframe":
        return AirframeForm


@login_required(login_url="account_login")
def reference_object_add(request, table):
    breadcrumbs = {
        "Home": reverse("home"),
        "Reference Tables": reverse("reference_tables"),
        "Add": "",
    }
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        formobj = evaluate_reference_form(table)
        form = formobj(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date_modified = timezone.now()
            obj.user = request.user
            obj.save()
            # messages.success(request, "Campaign successfully created.")
            return redirect("reference_tables")
    else:
        form = evaluate_reference_form(table)

    context = {
        "form": form,
        "returnURL": returnURL,
        "action": "Add",
        "breadcrumbs": breadcrumbs,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "v2/generic/data_entry_form.html", context)


@login_required(login_url="account_login")
def reference_object_update(request, link_id, table):
    refobj = evaluate_reference_object(table, link_id)
    obj = refobj.objects.get(id=link_id)
    formobj = evaluate_reference_form(table)
    form = formobj(instance=obj)
    returnURL = request.GET.get("returnUrl")
    breadcrumbs = {
        "Home": reverse("home"),
        "Reference Tables": reverse("reference_tables"),
        "Edit": "",
    }

    if request.method == "POST":
        form = formobj(request.POST, instance=obj)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.date_modified = timezone.now()
            form_obj.user = request.user
            form_obj.save()
            # messages.success(request, "Campaign successfully created.")
            return redirect("reference_tables")

    context = {
        "form": form,
        "action": "Edit",
        "returnURL": returnURL,
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "v2/generic/data_entry_form.html", context=context)


@login_required(login_url="account_login")
def reference_object_delete(request, link_id, table):
    refobj = evaluate_reference_object(table, link_id)
    obj = refobj.objects.get(id=link_id)
    obj.delete()
    # messages.success(request, "Campaign successfully deleted.")
    return redirect("reference_tables")
