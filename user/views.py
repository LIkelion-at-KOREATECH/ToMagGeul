from user.models import TMAuthor, TMUser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, AuthorCreationForm

def signup(request):
    user_form = UserCreationForm()
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if request.POST.get('is_author', ''):
                author_form = AuthorCreationForm()
                return render(request, 'createauthor.html', {'author_form':author_form, 'user':user})
            return redirect('signin')
    return render(request, 'signup.html', {'regi_form':user_form})

def createauthor(request):
    username = request.GET.get('name', '')
    author_form = AuthorCreationForm()
    if request.method == "POST":
        author_form = AuthorCreationForm(request.POST)
        if author_form.is_valid():
            author = author_form.save(commit=False)
            username = request.POST.get('name', '')
            user = get_object_or_404(TMUser, nickname=username)
            author.user = user
            user.is_author = True
            user.save()
            author.save()
            return redirect('thank')
 
    return render(request, 'createauthor.html', {'author_form':author_form})

def thankyou(request):
    return render(request, 'thankyou.html')


def signin(request):
    if str(request.user) != 'AnonymousUser':
        return redirect('mypage')  #로그인 한 상태에는 프로필 페이지로 감

    if request.method == "POST":
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('mypage')
    return render(request, 'signin.html')

@login_required
def signout(request):
    logout(request)
    return redirect('thank')


def profile(request,author):
    column = int(request.GET.get('column', '0'))
    isText = column == 0
    author = get_object_or_404(TMAuthor, author_name=author)
    return render(request, 'profile.html',{'author':author,'isText':isText})

@login_required
def mypage(request):
    column = int(request.GET.get('column', '0'))
    user = request.user
    series = []
    isText = False
    if column == 0:
        if user.is_author:
            series = user.tmauthor.series.all()
    elif column == 1:
        series = map(lambda x:x.tmseries,user.subs.all())
    elif column == 2:
        isText = True
        if user.is_author:
            series = user.tmauthor.text.all()
    elif column == 3:
        isText = True
        series = user.like.all()

    return render(request, 'mypage.html', {'series':series, 'isText':isText})