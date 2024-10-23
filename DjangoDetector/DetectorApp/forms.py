from django import forms
from django.forms import TextInput

from DetectorApp.models import *


class UserRegister(forms.Form):
    username = forms.CharField(max_length=30, label='Введите логин: ')
    password = forms.CharField(min_length=8, label='Введите пароль: ')
    repeat_password = forms.CharField(min_length=8, label='Повторите пароль: ')


class UserSearch(forms.Form):
    username = forms.CharField(max_length=30, label='Введите логин: ')
    password = forms.CharField(min_length=8, label='Введите пароль: ')


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['enter_user_name', 'image',]
        widgets = {
            'enter_user_name': TextInput(attrs={'placeholder': "Имя пользователя без ['  ']"}),
        }

