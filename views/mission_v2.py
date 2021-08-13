import os
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from ..models import Campaign, Mission, UserProfile, MissionFile, Comment
from ..forms import MissionForm, MissionFileForm


# ---------------- Mission -------------------------


@login_required(login_url="account_login")
def mission_v2(request, link_id):
    mission_queryset = Mission.objects.get(id=link_id)
    mission_files_queryset = mission_queryset.missionfile_set.all()
    combat_files_queryset = mission_queryset.combatflitefile_set.all()
    comments = mission_queryset.comments.all()
    packages = mission_queryset.package_set.all()
    targets = mission_queryset.target_set.all()
    threats = mission_queryset.threat_set.all()
    supports = mission_queryset.support_set.all()
    imagery = mission_queryset.missionimagery_set.all()
    user_profile = UserProfile.objects.get(user=request.user)
    
    form = MissionFileForm(initial = {'mission': mission_queryset, 'uploaded_by': request.user.id})

    breadcrumbs = {
        "Campaigns": reverse("campaigns"),
        mission_queryset.campaign.name: reverse(
            "campaign_detail_v2", args=(mission_queryset.campaign.id,)
        ),
        mission_queryset.name: "",
    }

    context = {
        "mission_object": mission_queryset,
        "package_object": packages,
        "target_object": targets,
        "threat_object": threats,
        "support_object": supports,
        "imagery_object": imagery,
        "mission_files": mission_files_queryset,
        "combat_files": combat_files_queryset,
        "isAdmin": user_profile.is_admin(),
        "comments": comments,
        'file_form': form,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "v2/mission/mission.html", context=context)


@login_required(login_url="account_login")
def mission_add_v2(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missionCount = campaign.mission_set.count() + 1
    returnURL = request.GET.get("returnUrl")
    image_url = request.build_absolute_uri(campaign.campaignImage.url)

    form_title = "Mission"

    form = MissionForm(
        initial={
            "campaign": campaign,
            "number": missionCount,
            "creator": request.user.id,
        }
    )

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.creator = request.user
            tmp.save()
            if tmp.notify_discord:
                tmp.create_discord_event(image_url, request)
            return HttpResponseRedirect(returnURL)

    context = {
        "form": form,
        "form_title": form_title,
        "link": link_id,
        "returnURL": returnURL,
    }
    return render(request, "v2/generic/data_entry_form.html", context=context)


@login_required(login_url="account_login")
def mission_update_v2(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")

    image_url = request.build_absolute_uri(mission.campaign.campaignImage.url)

    mission.create_discord_event(image_url, request)

    form_title = "Mission"

    form = MissionForm(instance=mission)

    if request.method == "POST":
        form = MissionForm(request.POST, request.FILES, instance=mission)
        
        if form.is_valid():
            saved_obj = form.save(commit=True)
            if saved_obj.notify_discord:
                saved_obj.create_discord_event(image_url, request)
            return HttpResponseRedirect(returnURL)

    context = {
        "form": form,
        "form_title": form_title,
        "link": link_id,
        "returnURL": returnURL,
    }
    return render(request, "v2/generic/data_entry_form.html", context=context)


@login_required(login_url="account_login")
def mission_delete_v2(request, link_id):
    mission = Mission.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")

    mission_files = mission.missionfile_set.all()

    # Check to see if an AO Image exists.
    if mission_files:
        for file in mission_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(file.mission_file)))
    
    if mission.discord_msg_id:
        mission.delete_discord_event()
    mission.delete()

    return HttpResponseRedirect(returnURL)


def mission_add_comment(request):
    # if this is a POST request we need to process the form data
    mission_id = request.GET.get("mission_id")
    returnURL = request.GET.get("returnUrl")

    if request.method == "POST":
        comment_data = request.POST.dict()
        comment = comment_data.get("comment_text")
        # Get the post object
        mission_object = Mission.objects.get(pk=mission_id)
        mission_object.comments.create(comment=comment, user=request.user)

    return HttpResponseRedirect(returnURL)

def mission_delete_comment(request, link_id):
    comment = Comment.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")
    
    comment.delete()
    
    return HttpResponseRedirect(returnURL)
    

def mission_file_add(request):
    # if this is a POST request we need to process the form data
    returnURL = request.GET.get('returnUrl')
    print('landed')
    form = MissionFileForm(request.POST, request.FILES)
    
    if form.is_valid():
        print('form valid')
        form.save(commit=True)
        return HttpResponseRedirect(returnURL)
        print('success00')
        
    print('fail')
    return HttpResponseRedirect(returnURL)

@login_required(login_url="account_login")
def mission_file_delete(request, link_id):
    mission_file_obj = MissionFile.objects.get(id=link_id)
    returnURL = request.GET.get("returnUrl")

    # Check to see if an AO Image exists.
    if mission_file_obj:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(mission_file_obj.mission_file)))

    mission_file_obj.delete()

    return HttpResponseRedirect(returnURL)
