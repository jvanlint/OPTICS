from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .view_decorators import allowed_users

from ..models import  Mission, Target
from ..forms import TargetForm

### Target Views ###

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def target_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = TargetForm(initial={'mission': mission})

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'target/target_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def target_update(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id
    form = TargetForm(instance=target)

    if request.method == "POST":
        form = TargetForm(request.POST, request.FILES, instance=target)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'form': form, 'link': missionID}
    return render(request, 'target/target_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def target_delete(request, link_id):
    target = Target.objects.get(id=link_id)
    missionID = target.mission.id

    if request.method == "POST":
        target.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': target}
    return render(request, 'target/target_delete.html', context=context)