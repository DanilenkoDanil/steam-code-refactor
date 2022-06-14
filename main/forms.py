from django import forms
from django.contrib import admin

from .models import Account, Key, Game


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = (
            'steam_login',
            'steam_password',
            'email',
            'email_password',
            'status',
            'country'
        )
        widgets = {
            'steam_login': forms.TextInput,
            'steam_password': forms.TextInput,
            'email': forms.EmailInput,
            'email_password': forms.TextInput,
            'country': forms.TextInput,


        }


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = (
            'sell_code',
            'name',
            'app_code',
            'country',
            'codes'
        )
        widgets = {
            'name': forms.TextInput,
            'steam_password': forms.TextInput,
            'country': forms.TextInput
        }








