from django.shortcuts import get_object_or_404, redirect, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Subscription, TMSeries, TMText, Comment
from .models import Genre
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
import math
import json
from .forms import *


# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all().order_by('-date_of_write')
    popular_tmts = TMText.objects.annotate(like_num=Count('like_users')).order_by('-like_num')[:5] # 좋아요 많은 순으로 5개 
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
    isSubs = False
    if user.is_authenticated:
        isSubs = user.subs.filter(tmseries=series)
    return render(request, 'tomaggeullist.html', {'series':series, 'isSubs':isSubs})
    
@login_required
def it_sounds_good(request,tmt_id): # test
    user = request.user
    tmtext=TMText.objects.get(text_id=tmt_id)

    if tmtext.like_users.filter(email=user.email).exists():
        tmtext.like_users.remove(user)
    else:
        tmtext.like_users.add(user)
    tmtext.save()
    context = {'heart_count' : tmtext.heart_num}
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
        # 입력받은 폼의 유효성 검사
        if tmtext_form.is_valid():
            # 객체를 생성하지 않고 저장
            tmtext = tmtext_form.save(commit=False)
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
            for i in genres:
                genre = Genre.objects.get(id = int(i))
                # 장르의 id 값으로 접근하여 값을 호출하여 add한다.
                tmtext.text_genre.add(genre)
            # 다시 객체를 저장한다.
            tmtext.save()
            return redirect('tmlist')
    return render(request, 'createText.html', {'tmtext_form':tmtext_form, 'genre':genre})
    
def tmseriescreate(request):
    genre = Genre.objects.all()
    series_form = TMSeriesCreationForm()
    if request.method == "POST":
        data = request.POST
        series_form = TMSeriesCreationForm(data)
        if series_form.is_valid():
            series = series_form.save(commit=False)
            series.writer = request.user.tmauthor
            series.save()
            genres = data.get('series_genre',[])
            for i in genres:
                g = Genre.objects.get(id = int(i))
                series.series_genre.add(g)
            series.save()
            
    return render(request, 'createSeries.html',{'genre':genre, 'series_form':series_form})

@login_required
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
    if request.method == 'POST':
        isDelete = request.POST.get('id',None)
        if not isDelete:
            comment = request.POST.get('comment','')
            cmt = Comment(comment_content=comment, tmtext = tmtext, tmuser = request.user)
            cmt.save()
        else:
            Comment.objects.get(id=isDelete).delete()


        return redirect('tmtext_detail', tmtext.text_id)

    return render(request, 'tomaggeul_detail.html', {'tmtext':tmtext})

def popup(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            email = request.POST.get('email','')
            password = request.POST.get('password','')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
        else:
            text = get_object_or_404(TMText, text_id = request.POST.get('select',0))
            print(text)
            #####해당 토막글 데이터 전송####
            ##############################
            pass
    return render(request, 'popup.html')