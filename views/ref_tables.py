from dataclasses import dataclass
from typing import Any
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
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


@dataclass(repr=False)
class Card:
    table_name: str
    heading_text: str
    heading_description: str
    data: Any


def get_cards():
    cards = [
        Card(
            table_name="status",
            heading_text="Campaign Status",
            heading_description="Used to describe the status of the campaign.",
            data=Status.objects.order_by("name")
        ),
        Card(
            table_name="terrain",
            heading_text="Terrain",
            heading_description="The list of available DCS Terrain for a campaign.",
            data=Terrain.objects.order_by("name")
        ),
        Card(
            table_name="waypoint_type",
            heading_text="Waypoint Types",
            heading_description="Types of actions performed at a given waypoint.",
            data=WaypointType.objects.order_by("name"),
        ),
        Card(
            table_name="flight_task",
            heading_text="Flight Tasks",
            heading_description="Tasks that can be performed by flights.",
            data=Task.objects.order_by("name"),
        ),
        Card(
            table_name="support_type",
            heading_text="Support Types",
            heading_description="The various support assets available in the mission.",
            data=SupportType.objects.order_by("name"),
        ),
        Card(
            table_name="threat_type",
            heading_text="Threat Types",
            heading_description="Classes that be assigned to a ground threat.",
            data=ThreatType.objects.order_by("name"),
        ),
        ]
    return cards


@login_required(login_url="login")
def reference_tables(request):
    airframe = Airframe.objects.order_by("name")  # Always update the airframe context
    if not request.htmx:
        # only update the other tables on initial non-htmx GET
        # terrain = Terrain.objects.order_by("name")
        # status = Status.objects.order_by("name")
        # waypoint_type = WaypointType.objects.order_by("name")
        # flight_task = Task.objects.order_by("name")
        # support_type = SupportType.objects.order_by("name")
        # threat_type = ThreatType.objects.order_by("name")

        cards = get_cards()

    page_num = request.GET.get("page", 1)
    airframes = Paginator(object_list=airframe, per_page=5).get_page(page_num)
    breadcrumbs = {"Home": reverse("home"), "Reference Tables": ""}

    if request.htmx:
        template = "v2/partials/airframes_partial.html"
        context = {"airframe_object": airframes}
    else:
        template = "v2/reference/reference_tables.html"
        context = {
            "airframe_object": airframes,
            "breadcrumbs": breadcrumbs,
            "cards": cards
        }
    return render(request, template_name=template, context=context)


def evaluate_reference_object(table):
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


@login_required(login_url="login")
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
            return redirect(returnURL or "reference_tables")
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


@login_required(login_url="login")
def reference_object_update(request, item_id=None, table=None):
    if request.method == "GET" and (not item_id and table):
        return HttpResponseBadRequest("no object id or table id")
    if item_id and table:
        reference_object = evaluate_reference_object(table)
        obj = reference_object.objects.get(id=item_id)
        form_object = evaluate_reference_form(table)
        form = form_object(request.POST or None, instance=obj)
        return_url = request.GET.get("returnUrl")
        url = reverse("reference_object_update", kwargs={"item_id": item_id, "table": table})
        breadcrumbs = {
            "Home": reverse("home"),
            "Reference Tables": reverse("reference_tables"),
            "Edit": "",
        }
        context = {
            "form": form,
            "action": "Edit",
            "returnURL": return_url,
            "breadcrumbs": breadcrumbs,
            "post_url": url,
            "table_name": table,
        }

    if request.method == "POST":
        form = form_object(request.POST, instance=obj)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.date_modified = timezone.now()
            form_obj.user = request.user
            form_obj.save()
            if request.htmx:
                context = {
                    "updated_item": obj,
                    "edit_url": url,
                    "table_name": table,
                }
                template = "V2/partials/reference_entry_detail.html"
                return render(request=request, template_name=template, context=context)
            else:
                return redirect("reference_tables")

    if request.htmx:
        template = "v2/partials/reference_entry_edit.html"
    else:
        template = "v2/generic/data_entry_form.html"

    return render(request=request, template_name=template, context=context)


@login_required(login_url="login")
def reference_object_delete(request, item_id, table):
    reference_obj = evaluate_reference_object(table)
    obj = reference_obj.objects.get(id=item_id)
    # obj.delete()
    # messages.success(request, "Campaign successfully deleted.")
    if request.htmx:
        return HttpResponse("")
    return redirect("reference_tables")
