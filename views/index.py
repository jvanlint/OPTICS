from django.shortcuts import render
from ..models import Campaign, Mission

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_campaigns = Campaign.objects.all().count()
    num_missions = Mission.objects.count()

    context = {
        'num_campaigns': num_campaigns,
        'num_missions': num_missions,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)

