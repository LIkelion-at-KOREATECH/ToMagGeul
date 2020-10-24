from django.shortcuts import get_object_or_404, render
from .models import Subscription, TMSeries, TMText
from .models import Genre
from django.core.paginator import Paginator
import math
from django.http import HttpResponse
import json


# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all().order_by('-date_of_write')
    all_genre = Genre.objects.all()
    paginator = Paginator(all_tmtext,5)
    page=1 if(request.GET.get('page') == None) else int(request.GET.get('page'))
    posts = paginator.get_page(page)
    page_range = 5 #페이지 범위 지정 예 1, 2, 3, 4, 5 / 6, 7, 8, 9, 10
    current_block = math.ceil(page/page_range) #해당 페이지가 몇번째 블럭인가
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    return render(request, 'mainpage.html', {'p_range':p_range , 'page': page,'posts':posts,'all_tmtext':posts, 'all_genre':all_genre})

def tmlist(request, pk):
    user = request.user
    series = get_object_or_404(TMSeries, series_id = pk)
    isSubs = user.subs.filter(tmseries=series)
    return render(request, 'tomaggeullist.html', {'series':series, 'isSubs':isSubs})

def popup(request):
    return render(request, 'popup.html')
    

def it_sounds_good(request,tmt_id): # test
    tmtext=TMText.objects.filter(text_id=tmt_id)
    heart_num = tmtext.values()[0]['heart_num']
    tmtext.update(heart_num = heart_num+1)
    context = {'heart_count' : heart_num}
    return HttpResponse(json.dumps(context), content_type='application/json')

def subscribe(request,series): # test
    user = request.user
    tmseries = get_object_or_404(TMSeries, series_id=series)
    subs = user.subs.filter(tmseries=series)
    state = "구독 취소되었습니다."
    if subs:
        subs.delete()
    else:
        subs = Subscription(tmuser = user, tmseries = tmseries)
        subs.save()
        state = "구독 신청하였습니다."
    context = {'substext' : state}
    
    return HttpResponse(json.dumps(context), content_type='application/json')

def tmtext_detail(request, tmt_id):
    tmtext=TMText.objects.filter(text_id=tmt_id)
    return render(request, 'tomaggeul_detail.html', {'tmtext':tmtext})
