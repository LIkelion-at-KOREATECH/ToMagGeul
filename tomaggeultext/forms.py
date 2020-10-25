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
                'placeholder' : "토막글 제목",
                'class':"input-title",
            }
        ))
    main_sentence = forms.CharField(
        max_length=200,
        label=('토막글 소개'),
        widget=forms.Textarea(
            attrs={
                'required' : 'True',
                'placeholder' : '토막글 소개',
                'class': 'tomag-introduce',
                'rows':'5',
            }
        )
    )
    text_content = forms.CharField(
        max_length = 1000,
        label=('토막글 쓰기'),
        widget= forms.Textarea(
            attrs={
                'required' : 'True',
                'placeholder': '토막글 쓰기',
                'class': 'tomag-write',
                'rows' : '15',
            }
        )
    )
    series = forms.ModelChoiceField(
        TMSeries.objects.all(),
        required=False,
        empty_label = "책 선택 안함", 
        label= ("책 선택하기"),
        widget=forms.Select(
            attrs ={
                'class': 'book-choice',
                'id' : 'book-choice',
            }
    )
    )
    class Meta:
        model = TMText
        fields = (
                    'text_title', 
                    'main_sentence', 
                    'text_content', 
                    )
class TMSeriesCreationForm(forms.ModelForm):
    series_title = forms.CharField(
        label = "책 제목 : ",
        max_length=30,
        widget=forms.TextInput(
            attrs = {
            'required' : 'True',
        }
        ))

    introduce = forms.CharField(
        label = "책 소개 : ",
        max_length=30,
        widget=forms.TextInput(
            attrs = {
                'required' : 'True',
            }
        )
    )
    
    class Meta:
        model = TMSeries
        fields = (
                    'series_title',
                    'introduce',
        )
                    