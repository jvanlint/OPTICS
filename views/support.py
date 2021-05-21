from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .view_decorators import  allowed_users

from ..models import  Mission, Support, Target
from ..forms import SupportForm

### Support Views ###

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def support_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = SupportForm(initial={'mission': mission})

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'support/support_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def support_update(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = support.mission.id
    form = SupportForm(instance=support)

    if request.method == "POST":
        form = SupportForm(request.POST, request.FILES, instance=support)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID}
    return render(request, 'support/support_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def support_delete(request, link_id):
    support = Support.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        support.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': support}
    return render(request, 'support/support_delete.html', context=context)
