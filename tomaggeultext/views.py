from django.shortcuts import render
from .models import TMText
from .models import Genre

# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all()
    all_genre = Genre.objects.all()
    return render(request, 'mainpage.html', {'all_tmtext':all_tmtext, 'all_genre':all_genre})

def createText(request):
    return render(request, 'createText.html')