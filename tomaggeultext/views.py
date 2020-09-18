from django.shortcuts import render
from .models import TMText

# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all()
    return render(request, 'mainpage.html', {'all_tmtext':all_tmtext},)