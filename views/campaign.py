

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .view_decorators import allowed_users

from ..models import Campaign
from ..forms import CampaignForm

# Campaign Views
@login_required(login_url='login')
def campaign(request):
    campaigns = Campaign.objects.order_by('id')

    context = {'campaigns': campaigns}

    return render(request, 'campaign/campaign.html', context=context)


@login_required(login_url='login')
def campaign_detail(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missions = campaign.mission_set.all().order_by('number')

    campaign.refresh_from_db()

    context = {'campaign': campaign, 'missions': missions}

    return render(request, 'campaign/campaign_detail.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def campaign_create(request):
    form = CampaignForm()

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully created.")
            return HttpResponseRedirect('/airops/campaign')

    context = {'form': form}
    return render(request, 'campaign/campaign_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def campaign_update(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    form = CampaignForm(instance=campaign)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Campaign successfully updated.")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'campaign/campaign_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def campaign_delete(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        campaign.delete()
        messages.success(request, "Campaign successfully deleted.")
        return HttpResponseRedirect(returnURL)

    context = {'item': campaign, 'returnURL': returnURL}
    return render(request, 'campaign/campaign_delete.html', context=context)
