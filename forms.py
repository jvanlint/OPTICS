from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# import GeeksModel from models.py
from .models import Campaign, Mission, Package, Flight, Threat, Aircraft, Target, Support, Waypoint

# create a ModelForm


class CampaignForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Campaign
        fields = "__all__"


class MissionForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Mission
        fields = "__all__"


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
        self.fields['targets'].queryset = target

    class Meta:
        model = Flight
        fields = "__all__"


class AircraftForm(ModelForm):
    def __init__(self, flights, *args, **kwargs):
        super(AircraftForm, self).__init__(*args, **kwargs)
        self.fields['flight'].queryset = flights

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


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
