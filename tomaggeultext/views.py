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
            for g in genres:
                # 장르의 id 값으로 접근하여 값을 호출하여 add한다.
                tmtext.text_genre.add(Genre.objects.get(id=int(g)))
            # 다시 객체를 저장한다.
            tmtext.save()
            return redirect('tmlist')
    return render(request, 'createText.html', {'tmtext_form':tmtext_form})
    
def tmseriescreate(request):
    # if request.method == "POST":
    return render(request, 'createSeries.html')

def tmlist(request):
    return render(request, 'tomaggeullist.html')
