from django import forms

from .models import TMText, TMSeries
from genre.models import Genre

class TMtextCreationForm(forms.ModelForm):
    text_title = forms.CharField(
        max_length = 30,
        label=('토막글 제목'),
        widget=forms.TextInput(
            attrs={
                'required' : ' True',
                'placeholder' : "Title",
                'class':"input-title-label",
            }
        ))
    main_sentence = forms.CharField(
        max_length=200,
        label=('토막글 소개'),
        widget=forms.TextInput(
            attrs={
                'required' : 'True',
                'placeholder' : 'Introduce',
                'class': 'tomag-introduce',
            }
        )
    )
    text_content = forms.CharField(
        max_length = 500,
        label=('토막글 쓰기'),
        widget= forms.TextInput(
            attrs={
                'required' : 'True',
                'placeholder': 'Content',
                'class': 'tomag-write'
            }
        )
    )
    text_genre = forms.ModelMultipleChoiceField(
        Genre.objects.all(),
        label = ("토막글 장르"),
        widget = forms.TextInput(
            attrs={
                'required' : 'True',
                'class': 'input-genre',
            }
        )
    )

    text_cover = forms.ImageField(
        label = ("책 표지 등록"),
    )

    series = forms.ModelChoiceField(
        TMSeries.objects.all(),
        label= ("책 선택하기"),
        widget=forms.Select(
            attrs ={
                'required' : 'True',
                'class': 'book-choice',
                'id' : 'book-choice',
            }
    )
    )
    # writer = forms.ModelChoiceField()
        # 글 생성 Form
    class Meta:
        model = TMText
        fields = (  'series',
                    'text_title', 
                    'main_sentence', 
                    'text_content', 
                    'text_genre', 
                    'writer',
                    'text_cover',)