from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .view_decorators import allowed_users

from ..models import  Mission, Package
from ..forms import  PackageForm

# Package Views


@login_required(login_url='login')
@never_cache
def package(request, link_id):
    package = Package.objects.get(id=link_id)
    flights = package.flight_set.all()

    context = {'packageObject': package, 'flightObject': flights}
    return render(request, 'package/package_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def package_create(request, link_id):
    mission = Mission.objects.get(id=link_id)

    form = PackageForm(initial={'mission': mission})

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/airops/mission/' + str(link_id))

    context = {'form': form, 'link': link_id}
    return render(request, 'package/package_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def package_update(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    form = PackageForm(instance=package)
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES, instance=package)
        print(request.path)
        if form.is_valid():
            form.save(commit=True)
            print("Form Saved!")
            return HttpResponseRedirect(returnURL)

    context = {'form': form, 'link': missionID, 'returnURL': returnURL}
    return render(request, 'package/package_form.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def package_delete(request, link_id):
    package = Package.objects.get(id=link_id)
    missionID = package.mission.id
    returnURL = request.GET.get('returnUrl')

    if request.method == "POST":
        package.delete()
        return HttpResponseRedirect('/airops/mission/' + str(missionID))

    context = {'item': package, 'returnURL': returnURL}
    return render(request, 'package/package_delete.html', context=context)
