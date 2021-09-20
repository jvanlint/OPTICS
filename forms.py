import pprint
from datetime import timezone, datetime

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Button,
    Reset,
    Column,
    Field,
    Row,
    Div,
    HTML,
)
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton
from airops import utils

# import GeeksModel from models.py
from airops.models import (
    Campaign,
    Mission,
    Package,
    Flight,
    Threat,
    Aircraft,
    Target,
    Support,
    Waypoint,
    MissionImagery,
    PackageImagery,
    FlightImagery,
    UserProfile,
    MissionFile,
    Squadron,
    Terrain,
    Status,
    WaypointType,
    SupportType,
    Task,
    ThreatType,
    Airframe,
)


# create a ModelForm


class DateInput(forms.DateInput):
    input_type = "date"


class CampaignForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Campaign
        fields = "__all__"
        widgets = {
            "start_date": DateInput(attrs={"style": "width: 150px;"}),
            "creator": forms.Select(attrs={"style": "width: 150px;"}),
            "dcs_map": forms.Select(attrs={"style": "width: 150px;"}),
            "status": forms.Select(attrs={"style": "width: 150px;"}),
        }
        exclude = (
            "modified_by",
            "created_by",
        )


class MissionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MissionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Mission
        fields = "__all__"
        widgets = {
            "mission_date": DateInput(attrs={"style": "width: 150px;"}),
            "mission_game_date": DateInput(attrs={"style": "width: 150px;"}),
        }
        exclude = (
            "discord_msg_id",
            "modified_by",
            "created_by",
        )

    def clean(self):
        # Combine the Mission date and time and set to UTC
        if self.cleaned_data["mission_date"] and self.cleaned_data["mission_time"]:
            self.cleaned_data["mission_date"] = datetime.combine(
                self.cleaned_data["mission_date"],
                self.cleaned_data["mission_time"],
                tzinfo=timezone.utc,
            )


class MissionFileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MissionFileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = MissionFile
        fields = "__all__"


class PackageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = Package
        fields = "__all__"
        exclude = (
            "modified_by",
            "created_by",
        )


class ThreatForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ThreatForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = Threat
        fields = "__all__"


class TargetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TargetForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = Target
        fields = "__all__"


class FlightForm(ModelForm):
    def __init__(self, target, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        self.fields["targets"].queryset = target
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Flight
        fields = "__all__"
        exclude = (
            "modified_by",
            "created_by",
        )


class AircraftForm(ModelForm):
    def __init__(self, flights, *args, **kwargs):
        super(AircraftForm, self).__init__(*args, **kwargs)
        self.fields["flight"].queryset = flights
        self.fields["pilot"].queryset = User.objects.order_by("username")
        self.fields["rio_wso"].queryset = User.objects.order_by("username")
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use

    class Meta:
        model = Aircraft
        fields = "__all__"


class SupportForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = Support
        fields = "__all__"


class WaypointForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WaypointForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = Waypoint
        fields = "__all__"


class MissionImageryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MissionImageryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = MissionImagery
        fields = "__all__"


class PackageImageryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PackageImageryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = PackageImagery
        fields = "__all__"


class FlightImageryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlightImageryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    # specify the name of model to use
    class Meta:
        model = FlightImagery
        fields = "__all__"


class TerrainForm(ModelForm):
    class Meta:
        model = Terrain
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "DCS terrain name.",
                    "class": "form-control",
                    "autofocus": None,
                }
            ),
        }


name_layout = Layout(
    InlineField(
        "name",
    )
)


class HxTerrainForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = name_layout

    class Meta:
        model = Terrain
        fields = ["name"]


class HxStatusForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-inline"
        self.helper.layout = name_layout

    class Meta:
        model = Status
        fields = ["name"]


class HxAirframeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = "row g-3"
        # self.helper.form_tag = True
        # self.helper.form_action = "action={{ post_url }}"
        self.helper.layout = Layout(
            InlineField(
                "name",
                "stations",
                "multicrew",
            ),
            FormActions(
                Submit("Save", "Save", css_class="btn btn-sm btn-primary"),
                Button("cancel","Cancel", css_class="btn-sm btn-danger"),
                Reset("reset_name", "Reset", css_class="btn btn-sm btn-warning"),
            ),
        )

    class Meta:
        model = Airframe
        fields = [
            "name",
            "stations",
            "multicrew",
        ]


'''
<form class="row g-3">
  <div class="col-auto">
    <label for="staticEmail2" class="visually-hidden">Email</label>
    <input type="text" readonly class="form-control-plaintext" id="staticEmail2" value="email@example.com">
  </div>
  <div class="col-auto">
    <label for="inputPassword2" class="visually-hidden">Password</label>
    <input type="password" class="form-control" id="inputPassword2" placeholder="Password">
  </div>
  <div class="col-auto">
    <button type="submit" class="btn btn-primary mb-3">Confirm identity</button>
  </div>
</form>
'''



class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Campaign status.",
                    "class": "form-control",
                    "autofocus": None,
                }
            ),
        }


class WaypointTypeForm(ModelForm):
    class Meta:
        model = WaypointType
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Waypoint type.",
                    "class": "form-control",
                    "autofocus": None,
                }
            ),
        }


class SupportTypeForm(ModelForm):
    class Meta:
        model = SupportType
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Support type.",
                    "class": "form-control",
                    "autofocus": None,
                }
            ),
        }


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Flight task.",
                    "class": "form-control",
                    "autofocus": None,
                }
            ),
        }


class ThreatTypeForm(ModelForm):
    class Meta:
        model = ThreatType
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Threat type.",
                    "class": "form-control",
                    "autofocus": None,
                }
            ),
        }


class AirframeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AirframeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Airframe
        # fields = ("__all__")
        fields = (
            "name",
            "stations",
            "multicrew",
        )
        exclude = ("user",)


class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):

    timezone = forms.ChoiceField(
        required=True,
        choices=utils.get_timezones(),
        initial=settings.TIME_ZONE,
    )

    class Meta:
        model = UserProfile
        fields = (
            "timezone",
            "squadron",
        )


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SignupForm(forms.ModelForm):  # Called by Allauth (see settings.py)
    timezone = forms.ChoiceField(
        required=True,
        choices=utils.get_timezones(),
        initial=settings.TIME_ZONE,
    )

    class Meta:
        model = UserProfile
        fields = (
            "squadron",
            "timezone",
        )

    def signup(self, request, user):  # Called by Allauth (see settings.py)
        user.profile.squadron = Squadron.objects.get(pk=request.POST["squadron"])

        user.profile.timezone = request.POST["timezone"]
        user.save()
