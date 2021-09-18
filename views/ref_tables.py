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


@login_required(login_url="login")
def reference_tables(request):
    airframe = Airframe.objects.order_by("name")  # Always update the airframe context
    if not request.htmx:
        # only update the other tables on initial non-htmx GET
        terrain = Terrain.objects.order_by("name")
        status = Status.objects.order_by("name")
        waypoint_type = WaypointType.objects.order_by("name")
        flight_task = Task.objects.order_by("name")
        support_type = SupportType.objects.order_by("name")
        threat_type = ThreatType.objects.order_by("name")

    page_num = request.GET.get("page", 1)
    airframes = Paginator(object_list=airframe, per_page=5).get_page(page_num)
    breadcrumbs = {"Home": reverse("home"), "Reference Tables": ""}

    if request.htmx:
        template = "v2/partials/airframes_partial.html"
        context = {"airframe_object": airframes}
    else:
        template = "v2/reference/reference_tables.html"
        context = {
            # "terrain_object": terrain,
            "status_objects": status,
            # "waypoint_type_object": waypoint_type,
            # "flight_task_object": flight_task,
            # "support_type_object": support_type,
            # "threat_type_object": threat_type,
            # "airframe_object": airframes,
            "breadcrumbs": breadcrumbs,
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


@login_required(login_url="login")
def reference_object_update(request, item_id=None, table=None):
    """
    GET -> return a form with an object instance
        check item_id and table not none
        get object instance
        get form for object

        if hx
            then a form partial,
        otherwise
            the full form page

    POST -> check valid and save the data
        if hx,
            return a detail view of the changed data
        otherwise,
            return redirect to "reference_tables"

    """
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
                }
                template = "V2/partials/data_entry_form_detail.html"
                return render(request=request, template_name=template, context=context)
            else:
                return redirect("reference_tables")

    if request.htmx:
        template = "v2/partials/data_entry_form_partial.html"
    else:
        template = "v2/generic/data_entry_form.html"

    return render(request=request, template_name=template, context=context)









@login_required(login_url="login")
def reference_object_delete(request, item_id, table):
    refobj = evaluate_reference_object(table, item_id)
    obj = refobj.objects.get(id=item_id)
    obj.delete()
    # messages.success(request, "Campaign successfully deleted.")
    return redirect("reference_tables")
