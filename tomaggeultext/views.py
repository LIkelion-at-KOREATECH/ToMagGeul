from django.shortcuts import get_object_or_404, render, redirect
from .models import Subscription, TMSeries, TMText
from genre.models import Genre
from django.core.paginator import Paginator
import math
from django.http import HttpResponse
import json
from .forms import *


# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all().order_by('-date_of_write')
    popular_tmts = TMText.objects.all().order_by('-heart_num')[:5] # 좋아요 많은 순으로 5개 
    all_genre = Genre.objects.all()
    
    paginator = Paginator(all_tmtext,5)
    page=1 if(request.GET.get('page') == None) else int(request.GET.get('page'))
    posts = paginator.get_page(page)
    page_range = 5 #페이지 범위 지정 예 1, 2, 3, 4, 5 / 6, 7, 8, 9, 10
    current_block = math.ceil(page/page_range) #해당 페이지가 몇번째 블럭인가
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    return render(request, 'mainpage.html', {'p_range':p_range , 'page': page,'posts':posts,'popular_tmts':popular_tmts, 'all_genre':all_genre})

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

def tmtextcreate(request):
    genre = Genre.objects.all()
    # form 불러오기
    tmtext_form = TMtextCreationForm()
    # request의 Method가 POST로 주어졌다면
    if request.method == "POST":
        # 입력받은 값을 data로 저장
        data = request.POST
        # 입력받은 값을 Form에 넣은 형태로 새로 저장
        tmtext_form = TMtextCreationForm(data)
        print("Form 전달")
        # 입력받은 폼의 유효성 검사
        if tmtext_form.is_valid():
            # 객체를 생성하지 않고 저장
            print("valid")
            tmtext = tmtext_form.save(commit=False)
            print(data)
            # series의 data를 get하는데 입력값이 없으면 None
            series = data.get('series',None)
            # series 값이 있다면
            if series:
                # 저장된 값의 seires를 입력받은 value값에서 객체를 접근하여 값을 호출하여 저장
                tmtext.series=TMSeries.objects.get(series_id=int(series[0]))
            # 작성자는 현재 로그인이 되어있는 작가
            tmtext.writer = request.user.tmauthor
            # 객체를 생성하여 저장
            tmtext.save()
            # 입력받은 장르 값을 get한다.
            genres = data.get('text_genre',[])
            # 장르는 다중 값임으로 모든 값에 대하여
            print(genres)
            for i in genres:
                genre = Genre.objects.get(id = int(i))
                # 장르의 id 값으로 접근하여 값을 호출하여 add한다.
                tmtext.text_genre.add(genre)
            # 다시 객체를 저장한다.
            tmtext.save()
            return redirect('tmlist')
        
        print("실패")
    return render(request, 'createText.html', {'tmtext_form':tmtext_form, 'genre':genre})
    
def tmseriescreate(request):
    # if request.method == "POST":
    return render(request, 'createSeries.html')

def tmlist(request):
    return render(request, 'tomaggeullist.html')
    
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
    tmtext=get_object_or_404(TMText, text_id=tmt_id)
    return render(request, 'tomaggeul_detail.html', {'tmtext':tmtext})
