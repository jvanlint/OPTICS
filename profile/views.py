from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User

import os
from django.conf import settings

from .models import Profile
from optics.opticsapp.models import Comment


@login_required(login_url='account_login')
def own_profile_view(request):
    # comments = Comment.objects.get(user=request.user)
    comments = Comment.objects.filter(user=request.user)

    context = {'comments': comments}
# Render the HTML template index.html with the data in the context variable
    return render(request, 'profile/profile.html', context=context)


@login_required(login_url='account_login')
def select_avatar(request):
    context = {}
    newfile = []
    files = os.listdir(os.path.join(settings.STATIC_ROOT, "optics/img/avatars/"))
    for file in files:
        newfile.append('optics/img/avatars/' + file)

    context = {'files': newfile}
    return render(request, 'profile/avatar_selection.html', context=context)


@login_required(login_url='account_login')
def change_avatar(request):
    avatar_image = request.GET.get('avatar')
    profile = Profile.objects.get(user=request.user)
    profile.profile_image = avatar_image
    profile.save()

    context = {}

    return render(request, 'profile/profile.html', context=context)


@login_required(login_url='account_login')
def user_profile_view(request, link_id):

    user_profile = User.objects.get(pk=link_id)

    # comments = Comment.objects.get(user=request.user)
    comments = Comment.objects.filter(user=user_profile)

    context = {'profile_object': user_profile, 'comments': comments}
# Render the HTML template index.html with the data in the context variable
    return render(request, 'profile/user_profile.html', context=context)
