from django.contrib import admin

from .forms import AccountForm, GameForm
from .models import Account, Key, SteamCode, Game, Telegram, Shop


@admin.register(Account)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'steam_login', 'steam_password', 'email', 'email_password', 'status', 'country'
    )
    form = AccountForm
    search_fields = ['steam_login']


@admin.register(Key)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('code', 'game', 'account')
    search_fields = ['code', 'account']


@admin.register(Game)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('sell_code', 'name', 'app_code', 'country', 'codes')
    search_fields = ['name', 'sell_code', 'app_code', 'country']
    form = GameForm


@admin.register(SteamCode)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('code', 'value', 'country', 'status', 'account')
    search_fields = ['code', 'value', 'country', 'status', 'account']


@admin.register(Telegram)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'name')


@admin.register(Shop)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'guid', 'seller_id')
