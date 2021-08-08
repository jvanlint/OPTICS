import pprint
from datetime import timezone, datetime

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from . import utils

# import GeeksModel from models.py
from .models import (
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
    UserProfile,
)


# create a ModelForm


class DateInput(forms.DateInput):
    input_type = "date"


class CampaignForm(ModelForm):

    # specify the name of model to use
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Campaign
        fields = "__all__"
        widgets = {
            "start_date": DateInput(
                attrs={
                    'style': 'width: 150px;'
                    }
            ),
            'creator': forms.Select(
                attrs={
                    'style': 'width: 150px;'
                    }
            ),
            'dcs_map': forms.Select(
                attrs={
                    'style': 'width: 150px;'
                    }
            ),
            'status': forms.Select(
                attrs={
                    'style': 'width: 150px;'
                    }
            ),
        }


class MissionForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Mission
        fields = "__all__"
        widgets = {"mission_date": DateInput(), "mission_game_date": DateInput()}
        exclude = ("discord_msg_id",)

    def clean(self):
        # Combine the Mission date and time and set to UTC
        if self.cleaned_data["mission_date"] and self.cleaned_data["mission_time"]:
            self.cleaned_data["mission_date"] = datetime.combine(
                self.cleaned_data["mission_date"],
                self.cleaned_data["mission_time"],
                tzinfo=timezone.utc,
            )




class PackageForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Package
        fields = "__all__"


class ThreatForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Threat
        fields = "__all__"


class TargetForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Target
        fields = "__all__"


class FlightForm(ModelForm):
    # specify the name of model to use
    def __init__(self, target, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        self.fields["targets"].queryset = target

    class Meta:
        model = Flight
        fields = "__all__"


class AircraftForm(ModelForm):
    def __init__(self, flights, *args, **kwargs):
        super(AircraftForm, self).__init__(*args, **kwargs)
        self.fields["flight"].queryset = flights
        self.fields["pilot"].queryset = User.objects.order_by("username")
        self.fields["rio_wso"].queryset = User.objects.order_by("username")

    # specify the name of model to use

    class Meta:
        model = Aircraft
        fields = "__all__"


class SupportForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Support
        fields = "__all__"


class WaypointForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Waypoint
        fields = "__all__"


class MissionImageryForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = MissionImagery
        fields = "__all__"


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
            "callsign",
            "timezone",
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
