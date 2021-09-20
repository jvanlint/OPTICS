from dataclasses import dataclass
from typing import Any
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.urls import reverse
from django.apps import apps

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
    HxAirframeForm,
    HxStatusForm,
    HxTerrainForm,
)


@dataclass(repr=False)
class Card:
    model_name: str
    heading_text: str
    heading_description: str
    display_fields: list[str]
    data: Any = None
    field_header_text: list[str] = None
    user_can_edit: bool = False
    user_can_add: bool = False
    user_can_delete: bool = False
    has_paginator: bool = False
    css_class: str = "col-lg-3 mx-4"


CARD_LIST = [
    Card(
        model_name="status",
        heading_text="Campaign Status",
        heading_description="Used to describe the status of the campaign.",
        display_fields=["name", "date_modified"],
        css_class="col-lg-4 mx-4",
        field_header_text=["Name", "Last Modified"],
        has_paginator=True,
    ),
    Card(
        model_name="terrain",
        heading_text="Terrain",
        heading_description="The list of available DCS Terrain for a campaign.",
        display_fields=["name"],
    ),
    # Card(
    #     model_name="waypoint_type",
    #     heading_text="Waypoint Types",
    #     heading_description="Types of actions performed at a given waypoint.",
    #     data=WaypointType.objects.order_by("name"),
    # ),
    # Card(
    #     model_name="flight_task",
    #     heading_text="Flight Tasks",
    #     heading_description="Tasks that can be performed by flights.",
    #     data=Task.objects.order_by("name"),
    # ),
    # Card(
    #     model_name="support_type",
    #     heading_text="Support Types",
    #     heading_description="The various support assets available in the mission.",
    #     data=SupportType.objects.order_by("name"),
    # ),
    # Card(
    #     model_name="threat_type",
    #     heading_text="Threat Types",
    #     heading_description="Classes that be assigned to a ground threat.",
    #     data=ThreatType.objects.order_by("name"),
    # ),
    Card(
        model_name="airframe",
        heading_text="Aircraft Types",
        heading_description="The airframes that can be assigned as aircraft in flights.",
        display_fields=["name", "stations", "multicrew"],
        css_class="col-lg-6 mx-4",
        has_paginator=True,
        field_header_text=["Type", "Wp Stations", "Multi-crew"],
    ),
]


def check_permissions(cards, user):
    for card in cards:
        card.user_can_edit = user.has_perm(f"airops.change_{card.model_name}")
        card.user_can_add = user.has_perm(f"airops.add_{card.model_name}")
        card.user_can_delete = user.has_perm(f"airops.delete_{card.model_name}")
    return cards


ITEMS_PER_PAGE = 5


def build_initial_paginators(cards):
    for card in cards:
        if card.has_paginator:
            paginator = Paginator(card.data, per_page=ITEMS_PER_PAGE)
            card.data = paginator.get_page(1)


def populate_card_data(card):
    model = apps.get_model("airops", card.model_name)
    # .values() is to convert query data to dict for template rendering
    # todo: replace "name" with ordinal_field for ordering
    card.data = model.objects.order_by("name").values()


@login_required(login_url="login")
def reference_tables(request):
    # logic problem here.
    # Initial request need to set all paginators to page 1
    # this reduces the card.data to ITEMS_PER_PAGE items
    #
    # if htmx call, then only the card in the call needs to be re-paginated
    # and the resultant card  rendered to template and returned.
    #
    # if NON htmx call, then initial paginator run again resetting all paginated
    # cards to page 1. Then setting the called card to page in call.
    breadcrumbs = {"Home": reverse("home"), "Reference Tables": ""}
    cards = CARD_LIST
    cards = check_permissions(cards, request.user)
    if not request.htmx:
        for card in cards:
            populate_card_data(card)  # full page refresh, update all cards.
        build_initial_paginators(cards)
    context = {
        "breadcrumbs": breadcrumbs,
        "cards": cards,
    }  # base non-htmx context - All cards
    page_num = request.GET.get("page", 1)
    page_model_name = request.GET.get("model")
    if page_model_name:  # A paginator has been triggered.
        # Get the card with the changing paginator
        paged_card = [card for card in cards if card.model_name == page_model_name][0]
        populate_card_data(paged_card)
        paged_card.data = Paginator(paged_card.data, per_page=ITEMS_PER_PAGE).get_page(
            page_num
        )

        if request.htmx:
            context = {
                "breadcrumbs": breadcrumbs,
                "card": paged_card,
            }  # HX context only requires one card
        else:
            # Swap the paged card into the cards
            cards = [paged_card for card in cards if card.model_name == page_model_name]
    if request.htmx:
        template = "v2/partials/reference_card_body_and_footer.html"
    else:
        template = "v2/reference/reference_tables.html"

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


def efr_1(table):  # Using dict method below, "Swap" coming in python 9.10
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


def evaluate_reference_form(table):
    return {
        "status": StatusForm,
        "terrain": TerrainForm,
        "waypoint_type": WaypointTypeForm,
        "flight_task": TaskForm,
        "support_type": SupportTypeForm,
        "threat_type": ThreatTypeForm,
        "airframe": AirframeForm,
    }[table]


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


'''
ordinal stuff will work itself out when an ordinal field is in the model as it 
will be bound and follow the context around.

zebra not working right now, check in html

entry detail partial template needs to know what fields 

'''

@login_required(login_url="login")
def reference_object_update(request, item_id=None, table=None):
    if request.method == "GET" and (not item_id and table):
        return HttpResponseBadRequest("no object id or table id")
    reference_object = evaluate_reference_object(table)
    obj = reference_object.objects.get(id=item_id)
    form_table = table
    form_object = evaluate_reference_form(form_table)
    form = form_object(request.POST or None, instance=obj)
    return_url = request.GET.get("returnUrl")

    url = reverse(
        "reference_object_update", kwargs={"item_id": item_id, "table": table}
    )
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
    if request.htmx and request.method == "GET":
        context.update(
            {
                "item_ordinal": request.GET.get("item_ordinal"),
                "item_zebra_css": request.GET.get("zebra"),
            }
        )

    if request.method == "POST":
        form = form_object(request.POST, instance=obj)
        if form.is_valid():
            form_obj = form.save(commit=False)  # initial form.save populates the form_obj with the new instance
            form_obj.date_modified = timezone.now()
            form_obj.user = request.user
            form_obj.save()
            if request.htmx:
                context = {
                    "item": obj,  #form.base_fields.keys() gives a list of the keys
# dont think the changed model instance is being loaded or displayed?
                    #from django.forms.models import model_to_dict
# model_to_dict(form_obj,fields=form.base_fields.keys())
                    #{'name': 'F-14B', 'stations': 8, 'multicrew': True}
                    # no need to check for what fields to show!
                    "edit_url": url,
                    "table_name": table,
                    "item_ordinal": form.data["item_ordinal"],
                    "item_zebra_css": form.data["item_zebra_css"],
                }
                template = "V2/partials/reference_entry_detail.html"
                return render(request=request, template_name=template, context=context)
            else:
                return redirect("reference_tables")

    if request.htmx:
        if table == "airframe":
            template = "v2/partials/airframe_entry_edit.html"
        else:
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


def reference_object_sort_order(request):
    if not request.htmx:
        raise Http404
    if request.method == "POST":
        print(request.POST)
        pass
        # will need to return the card values
