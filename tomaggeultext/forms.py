from django import forms

from .models import TMText, TMSeries
from genre.models import Genre

class TMtextCreationForm(forms.ModelForm):
        # 글 생성 Form
    class Meta:
        model = TMText
        fields = (  'text_title', 
                    'main_sentence', 
                    'text_content', 
                    'text_genre', 
                    'writer',
                    'series',)