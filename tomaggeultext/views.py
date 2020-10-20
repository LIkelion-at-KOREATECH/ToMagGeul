from django.shortcuts import render,redirect
from .models import TMText
from .models import Genre
from .models import TMSeries

# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all()
    all_genre = Genre.objects.all()
    return render(request, 'mainpage.html', {'all_tmtext':all_tmtext, 'all_genre':all_genre})

def tmtextcreate(request):
    all_tmseries = TMSeries.objects.all()
    return render(request, 'createText.html', {'all_tmseries':all_tmseries})
def tmlist(request):
    return render(request, 'tomaggeullist.html')
