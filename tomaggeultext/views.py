from django.shortcuts import render
from .models import TMText
from .models import Genre
#from django.http import HttpResponse
#import json

# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all()
    all_genre = Genre.objects.all()
    return render(request, 'mainpage.html', {'all_tmtext':all_tmtext, 'all_genre':all_genre})


def it_sounds_good(request,tmt_id): # test
    all_tmtext = TMText.objects.all()
    all_genre = Genre.objects.all()
    return render(request, 'mainpage.html', {'all_tmtext':all_tmtext, 'all_genre':all_genre})
    #context = {'likes_count' : '213', 'message' : '321'}
    #return HttpResponse(json.dumps(context), content_type='application/json')

def tmtext_detail(request, tmt_id):
    tmtext=TMText.objects.filter(text_id=tmt_id)
    return render(request, 'tomaggeul_detail.html', {'tmtext':tmtext})