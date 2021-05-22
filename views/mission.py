from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .view_decorators import allowed_users

from ..models import Campaign, Mission
from ..forms import MissionForm

# Mission Views

@login_required(login_url='login')
@never_cache
def mission(request, link_id):
    mission = Mission.objects.get(id=link_id)
    packages = mission.package_set.all()
    threat = mission.threat_set.all()
    target = mission.target_set.all()
    support = mission.support_set.all()

    context = {'mission_object': mission,
               'package_object': packages, 'threat_object': threat, 'target_object': target, 'support_object': support}
    return render(request, 'mission/mission_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def mission_create(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missionCount = campaign.mission_set.count() + 1
    returnURL = request.GET.get('returnUrl')

    form = MissionForm(initial={'campaign': campaign, 'number': missionCount})
    #form.base_fields['number'].initial = missionCount

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/campaign/' + str(link_id))

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'mission/mission_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def mission_update(request, link_id):
    mission = Mission.objects.get(id=link_id)
    form = MissionForm(instance=mission)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES, instance=mission)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': link_id, 'returnURL': returnURL}
    return render(request, 'mission/mission_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def mission_delete(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get('returnUrl')
    campaignID = mission.campaign.id

    if request.method == "POST":
        mission.delete()
        return HttpResponseRedirect('/airops/campaign/' + str(campaignID))

    context = {'item': mission, 'returnURL': returnURL}
    return render(request, 'mission/mission_delete.html', context=context)
