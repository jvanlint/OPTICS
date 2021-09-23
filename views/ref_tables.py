from dataclasses import dataclass
from typing import Any

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ..forms import (
    TerrainForm,
    StatusForm,
    TaskForm,
    SupportTypeForm,
    WaypointTypeForm,
    ThreatTypeForm,
    AirframeForm,
)
from ..models import (
    Status,
)

DEFAULT_ITEMS_PER_PAGE = 5


@dataclass(repr=False)
class Card:
    model_name: str  # Class Name of the model to display on this card Capitalisation important
    heading_text: str  # The large heading text (normally the model name)
    heading_description: str  # The smaller model description text
    data: Any = None  # Will be populated by view
    display_fields: list[
        str
    ] = None  # List of the FieldNames to display (overrides the ones defined in model)
    field_header_text: list[
        str
    ] = None  # List of text for field headers (overrides the ones defined in model)
    user_can_edit: bool = False  # Permission flags
    user_can_add: bool = False
    user_can_delete: bool = False
    has_paginator: bool = False  # Include a paginator on this card
    paginator_items: int = DEFAULT_ITEMS_PER_PAGE  # Number of items per page
    css_class: str = "col-lg-4 mx-3"  # raw css appended to <card class=


@dataclass
class EditReturnCard:
    model_name: str = None
    user_can_edit: bool = True
    user_can_delete: bool = False


CARD_LIST = [
    Card(
        model_name="Status",
        heading_text="Campaign Status",
        heading_description="Used to describe the status of the campaign.",
        css_class="col-lg-4 mx-4",
    ),
    Card(
        model_name="StatusWithDate",  # DEMO card only!
        heading_text="Campaign Status + date",
        heading_description="Used to describe the status of the campaign.",
        css_class="col-lg-4 mx-4",
    ),
    Card(
        model_name="Terrain",
        heading_text="Terrain",
        heading_description="The list of available DCS Terrain for a campaign.",
    ),
    Card(
        model_name="WaypointType",
        heading_text="Waypoint Types",
        heading_description="Types of actions performed at a given waypoint.",
        has_paginator=True,
        paginator_items=6,
    ),
    Card(
        model_name="Task",
        heading_text="Flight Tasks",
        heading_description="Tasks that can be performed by flights.",
    ),
    Card(
        model_name="SupportType",
        heading_text="Support Types",
        heading_description="The various support assets available in the mission.",
    ),
    Card(
        model_name="ThreatType",
        heading_text="Threat Types",
        heading_description="Classes that be assigned to a ground threat.",
    ),
    Card(
        model_name="Airframe",
        heading_text="Aircraft Types",
        heading_description="The airframes that can be assigned as aircraft in flights.",
        css_class="col-lg-6 mx-4",
        has_paginator=True,
        field_header_text=["OVType", "OVWp Stations", "OVMulti-crew"],
    ),
]


class StatusWithDate(Status):
    def display_data(self):
        return [self.name, self.date_modified]

    @staticmethod
    def field_headers():
        return ["Name", "Last Modified"]

    class Meta:
        proxy = True  # https://docs.djangoproject.com/en/3.2/topics/db/models/#proxy-models


def check_permissions(cards, user):
    for card in cards:
        card.user_can_edit = user.has_perm(f"airops.change_{card.model_name}")
        card.user_can_add = user.has_perm(f"airops.add_{card.model_name}")
        card.user_can_delete = user.has_perm(f"airops.delete_{card.model_name}")
    return cards


def build_initial_paginators(cards):
    for card in cards:
        if card.has_paginator:
            paginator = Paginator(card.data, per_page=card.paginator_items)
            card.data = paginator.get_page(1)


def populate_card_data(card):
    model = apps.get_model("airops", card.model_name)
    # todo: replace "name" with ordinal_field for ordering
    queryset_data = model.objects.order_by("name")

    return queryset_data


def populate_card_field_headers(card):
    if not card.field_header_text:
        model = apps.get_model("airops", card.model_name)
        return model.field_headers()
    else:
        return card.field_header_text


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
    if not request.htmx:  # full page refresh, update all cards.
        for card in cards:
            card.data = populate_card_data(card)
            card.field_header_text = populate_card_field_headers(card)
        build_initial_paginators(cards)
        context = {
            "breadcrumbs": breadcrumbs,
            "cards": cards,  # base non-htmx context - All cards
        }
    page_num = request.GET.get("page", 1)
    page_model_name = request.GET.get("model")
    if page_model_name:  # A paginator has been triggered.
        # Get the card with the changing paginator
        paged_card = [card for card in cards if card.model_name == page_model_name][0]
        paged_card.data = populate_card_data(paged_card)
        paged_card.data = Paginator(
            paged_card.data, per_page=paged_card.paginator_items
        ).get_page(page_num)

        if request.htmx:
            context = {
                "breadcrumbs": breadcrumbs,
                "card": paged_card,
            }  # HX context only requires one card
        else:
            # Swap the paged card into the cards
            cards = [paged_card for card in cards if card.model_name == page_model_name]
    if request.htmx:
        template = "v2/reference/partials/reference_card_body_and_footer.html"
    else:
        template = "v2/reference/reference_tables.html"

    return render(request, template_name=template, context=context)


def evaluate_reference_object(table):
    return NotImplementedError()  # debugging
    # apps.get_model("airops", model_name) does the same thing
    # return {
    #     "status": Status,
    #     "terrain": Terrain,
    #     "waypoint_type": WaypointType,
    #     "flight_task": Task,
    #     "support_type": SupportType,
    #     "threat_type": ThreatType,
    #     "airframe": Airframe,
    #     "status_with_date": StatusWithDate,
    # }[table]


def evaluate_reference_form(card_name):  # Capitalisation important! card (table) names are .lower()
    return {
        "status": StatusForm,
        "terrain": TerrainForm,
        "waypointtype": WaypointTypeForm,
        "task": TaskForm,
        "supporttype": SupportTypeForm,
        "threattype": ThreatTypeForm,
        "airframe": AirframeForm,
        "statuswithdate": StatusForm,  # Must include any Model Proxy's and assign a form
    }[card_name]
    # could possibly use django's modelform_factory() with data from the card to generate forms on the fly


@login_required(login_url="login")
def reference_object_add(request, card_name):  # todo: Update Add to new inline forms.
    breadcrumbs = {
        "Home": reverse("home"),
        "Reference Tables": reverse("reference_tables"),
        "Add": "",
    }
    return_url = request.GET.get("returnUrl")
    modelform_object = evaluate_reference_form(card_name.lower())
    if request.method == "POST":
        form = modelform_object(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date_modified = timezone.now()
            obj.user = request.user
            obj.save()
            return redirect(return_url or "reference_tables")
    else:
        form = modelform_object

    context = {
        "form": form,
        "returnURL": return_url,
        "action": "Add",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "v2/generic/data_entry_form.html", context)


@login_required(login_url="login")
def reference_object_update(request, item_id=None, card_name=None):
    if request.method == "GET" and (not item_id and card_name):
        return HttpResponseBadRequest("no object id or card_name id")
    object_model = apps.get_model("airops", card_name)
    object_to_update = object_model.objects.get(id=item_id)
    form_table = card_name.lower()
    modelform_object = evaluate_reference_form(form_table)
    form = modelform_object(request.POST or None, instance=object_to_update)
    return_url = request.GET.get("returnUrl")
    url = reverse("reference_object_update", kwargs={"item_id": item_id, "card_name": card_name})
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
        "card_name": card_name,
    }
    if request.htmx and request.method == "GET":
        context.update(
            {
                "item_zebra_css": request.GET.get("zebra"),
            }
        )

    if request.method == "POST":
        form_obj = ""
        # form = form_object(request.POST, instance=object_to_update)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.date_modified = timezone.now()
            form_obj.user = request.user
            form_obj.save()

        if request.htmx:
            return_card = EditReturnCard(model_name=card_name)
            return_card.user_can_delete = request.user.has_perm(f"airops.delete_{card_name}")
            context = {
                "item": form_obj,
                "edit_url": url,
                "table_name": card_name,
                "zebra": form.data["item_zebra_css"],
                "item.id": item_id,
                "item.name": form_obj.name,
                "card": return_card,  # need this to enable "action" button(s)
            }
            template = "V2/reference/partials/reference_entry_detail.html"
            return render(request=request, template_name=template, context=context)
        else:
            return redirect("reference_tables")

    if request.htmx:
        template = "v2/reference/partials/reference_entry_edit.html"
    else:
        template = "v2/generic/data_entry_form.html"

    return render(request=request, template_name=template, context=context)


@login_required(login_url="login")
def reference_object_delete(request, item_id, card_name):
    reference_obj = apps.get_model("airops", card_name)
    obj = reference_obj.objects.get(id=item_id)
    obj.delete()
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
        # todo: Add ordinal field to tables and work out how to implement this
