from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View

import time
from main.models import Account, Key, Game
from . import mail

from . import send_gift
from . import api


class DynamicCodeLoad(View):

    def get(self, request, *args, **kwargs):
        login = request.GET.get('account')
        account = get_user_by_login(login)
        code = mail.get_code(account)
        obj = {
            'code': code
        }
        return JsonResponse({'data': obj})


class DynamicAccountLoad(View):

    def get(self, request, *args, **kwargs):
        code = request.GET.get('uniquecode')
        key = get_key(code)
        print(key)
        if key is False:
            info = api.check_code(code)
            if info['retval'] == 0:

                game = get_game(info['id_goods'])
                game_code = game.app_code

                buy = get_user_by_country('Buy', game.country)
                gift = get_user_by_country('Gift', game.country)

                game_link = f'https://store.steampowered.com/app/{game_code}'
                try:
                    final_account = send_gift.full_send(buy, gift, game_link, game.country)
                except Exception as e:
                    print(e)
                    buy.status = False
                    buy.save()
                    gift.status = False
                    gift.save()
                    buy = get_user_by_country('Buy', game.country)
                    gift = get_user_by_country('Gift', game.country)
                    try:
                        final_account = send_gift.full_send(buy, gift, game_link, game.country)
                    except Exception as e:
                        print(e)
                        html = f"Произошла ошибка, пожалуйста обратитесь к продавцу! Ваш код - {code}"
                        data = {
                            "login": html,
                            "password": html
                        }
                        print('Success')
                        return JsonResponse(data)

                key = Key(code=code, account=final_account, game=game)
                key.save()
                final_account.status = True
                final_account.save()

                data = {
                    "login": final_account.steam_login,
                    "password": final_account.steam_password
                }
                print('Success')
                return JsonResponse(data=data)
        else:

            data = {
                "login": key.account.steam_login,
                "password": key.account.steam_password
            }
            print('Success')
            return JsonResponse(data=data)


def get_user_by_login(login: str) -> Account:
    return Account.objects.filter(steam_login=login)[0]


def get_user(user_type: str) -> Account:
    return Account.objects.filter(type=user_type, status=None)[0]


def get_user_by_country(user_type: str, country: str) -> Account:
    return Account.objects.filter(type=user_type, country=country, status=None)[0]


def get_game(product_code: str) -> Game:
    return Game.objects.filter(sell_code=product_code)[0]


def get_key(key: str):
    try:
        return Key.objects.filter(code=key)[0]
    except IndexError:
        return False


def index(request):
    code = request.GET.get('uniquecode')
    key = get_key(code)
    if key is False:
        info = api.check_code(code)
        if info['retval'] == 0:

            game = get_game(info['id_goods'])
            game_code = game.app_code

            image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
            game_link = f'https://store.steampowered.com/app/{game_code}'

            return render(request, 'main/account.html',
                          {'game_name': game.name,
                           'game_link': game_link,
                           'image_link': image_link,
                           'code': code
                           })
        else:
            html = f"Код {code} не действителен!"
            return HttpResponse(html)
    else:

        game_code = key.game.app_code
        image_link = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_code}/header.jpg"
        game_link = f'https://store.steampowered.com/app/{game_code}'

        return render(request, 'main/account.html',
                      {'game_name': key.game.name,
                       'game_link': game_link,
                       'image_link': image_link,
                       'code': code,
                        })
