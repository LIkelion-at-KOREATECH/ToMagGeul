from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from .models import TMUser, TMAuthor
from .managers import TMUserManager
from genre.models import Genre

class UserCreationForm(forms.ModelForm):
    # 사용자 생성 폼
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Email address'),
                'required': 'True',
            }
        ),
        max_length = 255,
        error_messages={'required': '이메일을 입력해 주세요.',
                        'invalid' : '이미 사용중인 이메일입니다.'}
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        ),
        max_length = 30,
        min_length = 8,
        # help_text='8~30 characters required'
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        ),
        max_length = 30,
        min_length = 8,
    )
    nickname = forms.CharField(
        label=_('Nickname'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Nickname'),
                'required': 'True',
            }
        ),
        min_length = 2,
        max_length = 50
    )

    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
                'required': 'True',
            }
        ),
        max_length = 30
    )

    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        widget=forms.SelectDateWidget(
            attrs={
                'type' : 'date',
                'class': 'form-control',
                'required': 'True',
            },
            years=range(2020,1900,-1)
        ),
    )

    phone_number = forms.RegexField(
        label=_('Phone Number'),
        regex=r'^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$',
        widget=forms.TextInput(
            attrs={
                'type' : 'text',
                'class': 'form-control',
                'placeholder': '000-0000-0000',
            }
        ),
        max_length = 13
    )

    address = forms.CharField(
        label=_('Address'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('address'),
            }
        ),
        max_length = 200
    )

    prefer_genre = forms.ModelMultipleChoiceField(Genre.objects)

    is_author = forms.BooleanField(
        label=_('Register Author'),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'onchange':"setDisplay()",
            }
        )
    )

    class Meta:
        model = TMUser
        fields = (  'email', 
                    'password1', 
                    'password2', 
                    'nickname', 
                    'name', 
                    'date_of_birth',
                    'phone_number',
                    'address',
                    'prefer_genre')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = TMUserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthorCreationForm(forms.ModelForm):

    # 작가 생성 폼
    class Meta:
        model = TMAuthor
        fields = (  'author_name', 
                    'introduce', 
                    'page_link', 
                    'sns_link', 
                    'portfolio',)

# class UserChangeForm(forms.ModelForm):
#     # 비밀번호 변경 폼
#     password = ReadOnlyPasswordHashField(
#         label=_('Password')
#     )

#     class Meta:
#         model = TMUser
#         fields = ('email', 'password', 'last_name', 'first_name', 'is_active', 'is_superuser')

#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]