from django.shortcuts import render,redirect
from .forms import *
from .models import TMText
from .models import Genre
from .models import TMSeries

# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all()
    all_genre = Genre.objects.all()
    return render(request, 'mainpage.html', {'all_tmtext':all_tmtext, 'all_genre':all_genre})

def tmtextcreate(request):
    # writer = request.GET.get.('author', '')
    all_tmseries = TMSeries.objects.values_list()
    tmtext_form = TMtextCreationForm()
    if request.method == "POST":
        tmtext_form = TMtextCreationForm(request.POST)
        if tmtext_form.is_valid():
            tmtext = tmtext_form.save(commit=False)
            tmtext.writer = writer
            tmtext_form.save()
            return redirect('tomaggeullist')
    return render(request, 'createText.html', {'all_tmseries':all_tmseries ,'tmtext_form':tmtext_form})
    
def tmseriescreate(request):
    # if request.method == "POST":
    return render(request, 'createSeries.html')

def tmlist(request):
    return render(request, 'tomaggeullist.html')
