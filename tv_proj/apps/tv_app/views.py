from django.shortcuts import render, HttpResponse, redirect
from .models import TV
from time import strftime, strptime
from django.contrib import messages

#rendering first page
def index(request): 
    context = {
        "Shows": TV.objects.all()
    }
    return render(request, 'tv_app/index.html', context)

#render add show page
def add_show_page(request):
    return render(request, 'tv_app/index2.html')

#validate show info and create
def add_show(request):
    errors = TV.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/shows/new")
    else:
        showTitle = request.POST['title']
        showNetwork = request.POST['network']
        showRD = request.POST['release_date']
        showDesc = request.POST['desc']
        new_tv = TV.objects.create(title=showTitle, network=showNetwork, release_date=showRD, desc=showDesc)
        messages.success(request, "Successfully added show!")
        return redirect(f'/shows/{new_tv.id}')

#go to selected show
def view_show(request, num):
    show_id = TV.objects.get(id=num)
    release = show_id.release_date.strftime('%d/%m/%Y')
    context = {
        "show_release": release,
        "show_id": show_id,
        "show_updated": show_id.updated_at
    }
    return render(request, 'tv_app/index3.html', context)

#edit show page
def edit_show_page(request, num):
    show = TV.objects.get(id=num)
    context={
        "show": show
    }
    return render(request, 'tv_app/index4.html', context)

#validate and edit show
def edit_show(request, num):
    errors = TV.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/shows/{num}/edit")
    else:
        update_show = TV.objects.get(id=num)
        update_show.title = request.POST['title']
        update_show.network = request.POST['network']
        update_show.release_date = request.POST['release_date']
        update_show.desc = request.POST['desc']
        update_show.save()
        return redirect(f"/shows/{num}")

#remove the show from DB
def remove_show(request, num):
    show = TV.objects.get(id=num)
    show.delete()
    return redirect("/shows")
    