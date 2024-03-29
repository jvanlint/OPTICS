# For deleting physical files (like images) when campaign is deleted.
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from ..forms import CampaignForm
from ..models import Campaign, UserProfile, Comment


@login_required(login_url="account_login")
def campaigns_all(request):
    """
    Retrieves all campaign objects and returns a HTML file displaying all objects.

    Args:
            request: The Django request object.

    Returns:
            A rendered HTML page with context containing campaign data, whether the user is an admin and breadcrumbs.
    """

    #campaigns_queryset = Campaign.objects.order_by('status', 'name')
    campaigns_queryset = Campaign.objects.filter(status__name__iexact="Active").order_by('status', 'name')
    user_profile = UserProfile.objects.get(user=request.user)

    breadcrumbs = {"Home": ""}

    context = {
        "campaigns": campaigns_queryset,
        "isAdmin": user_profile.is_admin(),
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "v2/campaign/campaigns.html", context=context)
    
@login_required(login_url="account_login")
def campaigns_filter(request):
    filter = request.GET.get("filter")
    
    if filter == "All":
        campaigns_queryset = Campaign.objects.order_by('status', 'name')
    else:
        campaigns_queryset = Campaign.objects.filter(status__name__iexact=filter).order_by('status', 'name')
    
    
    
    user_profile = UserProfile.objects.get(user=request.user)
    
    breadcrumbs = {"Home": ""}
    
    context = {
        "campaigns": campaigns_queryset,
        "isAdmin": user_profile.is_admin(),
        "breadcrumbs": breadcrumbs,
    }
    
    return render(request, "v2/campaign/includes/campaign_card.html", context=context)
    

@login_required(login_url="account_login")
def campaign_detail_v2(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    missions = campaign.mission_set.all().order_by("number")
    comments = campaign.comments.all()
    user_profile = UserProfile.objects.get(user=request.user)

    breadcrumbs = {"Campaigns": reverse_lazy("campaigns"), campaign.name: ""}

    campaign.refresh_from_db()

    context = {
        "campaign_object": campaign,
        "mission_object": missions,
        "isAdmin": user_profile.is_admin(),
        "comments": comments,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "v2/campaign/campaign.html", context=context)


@login_required(login_url="account_login")
def campaign_add_v2(request):

    breadcrumbs = {"Campaigns": reverse("home"), "Add": ""}

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.modified_by = request.user
            obj.created_by = request.user
            obj.save()
            # messages.success(request, "Campaign successfully created.")
            return HttpResponseRedirect(reverse_lazy("campaigns"))
    else:
        form = CampaignForm(initial={"creator": request.user.id})

    context = {
        "form": form,
        "action": "Add",
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "v2/campaign/campaign_form.html", context)


@login_required(login_url="account_login")
def campaign_update_v2(request, link_id):
    campaign = Campaign.objects.get(id=link_id)
    form = CampaignForm(instance=campaign)
    return_url = request.GET.get("returnUrl")
    breadcrumbs = {
        "Campaigns": reverse_lazy("campaigns"),
        campaign.name: reverse_lazy("campaign_detail_v2", args=(campaign.id,)),
        "Edit": "",
    }

    if request.method == "POST":
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        print(request.path)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.modified_by = request.user
            obj.save()
            # messages.success(request, "Campaign successfully updated.")
            return HttpResponseRedirect(return_url)

    context = {
        "form": form,
        "link": link_id,
        "returnURL": return_url,
        "breadcrumbs": breadcrumbs,
        "action": "Edit",
    }
    return render(request, "v2/campaign/campaign_form.html", context=context)


@login_required(login_url="account_login")
def campaign_delete_v2(request, link_id):
    campaign = Campaign.objects.get(id=link_id)

    # Delete the campaign thumbnail before deleting the actual DB record.
    # Check to see if a campaign thumbnail exists.
    if campaign.campaignImage:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(campaign.campaignImage)))

    # Check to see if an AO Image exists.
    if campaign.aoImage:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(campaign.aoImage)))

    campaign.delete()
    # messages.success(request, "Campaign successfully deleted.")

    return HttpResponseRedirect(return_url)


@login_required(login_url="account_login")
def campaign_redirect(request):
    return redirect('campaigns')

# ---------------- Campaign Comments -------------------------
def campaign_add_comment(request):

    campaign_id = request.GET.get('campaign_id')
    
    if request.method == 'POST':
        comment_data = request.POST.dict()
        comment = comment_data.get("comment_text")
        # Get the post object
        campaign = Campaign.objects.get(pk=campaign_id)
        campaign.comments.create(comment=comment, 
                                 user=request.user)
    
    context = campaign_all_comments(campaign_id)
    
    return render(request, "v2/campaign/includes/comments.html", context=context)
        

def campaign_delete_comment(request, link_id):
    
    campaign_id = request.GET.get('campaign_id')
    comment = Comment.objects.get(id=link_id)
    
    comment.delete()
    
    context = campaign_all_comments(campaign_id)
    
    return render(request, "v2/campaign/includes/comments.html", context=context)
    
def campaign_edit_comment(request, link_id):
    comment = Comment.objects.get(id=link_id)
    
    campaign_id = request.GET.get('campaign_id')
    campaign = Campaign.objects.get(id=campaign_id)
    
    context = {
        "comment": comment,
        "campaign_object": campaign,
    }
    
    return render(request, "v2/campaign/includes/comment_edit.html", context=context)

def campaign_show_comments(request):
    campaign_id = request.GET.get('campaign_id')
    context = campaign_all_comments(campaign_id)
    
    return render(request, "v2/campaign/includes/comments.html", context=context)

def campaign_update_comment(request, link_id):
    comment = Comment.objects.get(id=link_id)
    campaign_id = request.GET.get('campaign_id')
    
    if request.method == 'POST':
        comment_data = request.POST.dict()
        comment_text = comment_data.get("comment_edit_text")
        comment.comment = comment_text
        comment.save()

    context = campaign_all_comments(campaign_id)
    
    return render(request, "v2/campaign/includes/comments.html", context=context)
    
def campaign_all_comments(campaign_id):
    
    campaign = Campaign.objects.get(id=campaign_id)
    comments = campaign.comments.all()
    
    context = {
        "comments": comments,
        "campaign_object": campaign,
    }
    
    return context
# **** End Campaigns Code *****