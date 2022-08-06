import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from apps.airops.forms import ProfileForm
from apps.airops.models import Comment, UserProfile
from collections import namedtuple


@login_required(login_url="account_login")
def own_profile_view(request):
    comments = Comment.objects.filter(user=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    breadcrumbs = {"Campaigns": reverse("campaigns"), "Own Profile": ""}
    context = {
        "comments": comments,
        "breadcrumbs": breadcrumbs,
        "profile_form": profile_form,
    }
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("own_profile")
        else:
            messages.error(request, "Please correct the error below.")
    return render(request, "v2/profile/profile.html", context=context)


@login_required(login_url="account_login")
def select_avatar(request):
    context = {}
    new_file = []
    avatar_location = "assets/img/avatars/"
    files = os.listdir(os.path.join(settings.STATIC_ROOT, avatar_location))
    for file in files:
        new_file.append(avatar_location + file)

    context = {"files": new_file}
    return render(request, "v2/profile/avatar_selection.html", context=context)


@login_required(login_url="account_login")
def change_avatar(request):
    avatar_image = request.GET.get("avatar")
    profile = UserProfile.objects.get(user=request.user)
    profile.profile_image = avatar_image
    profile.save()

    comments = Comment.objects.filter(user=request.user)

    context = {"comments": comments}

    return render(request, "v2/profile/avatar_selection.html", context=context)


@login_required(login_url="account_login")
def user_profile_view(request, link_id):

    user_profile = User.objects.get(pk=link_id)
    breadcrumbs = {"Campaigns": reverse("campaigns"), "User Profile": ""}

    comments = Comment.objects.filter(user=user_profile)

    context = {
        "profile_object": user_profile,
        "comments": comments,
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "v2/profile/user_profile.html", context=context)
