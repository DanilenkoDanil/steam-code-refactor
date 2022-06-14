from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from background_task import background
from background_task.models import Task

from main.models import Account, Key, Game, Shop
from . import mail

from . import send_gift
from . import api


def get_shops() -> Shop:
    return Shop.objects.all()


@background
def new_account(info, code):
    game = get_game(info['id_goods'])
    game_code = game.app_code


    account = get_user_by_country(game.country)

    game_link = f'https://store.steampowered.com/app/{game_code}'

    account.status = False
    account.save()

    try:

        final_account = send_gift.full_send(account, game, game_link, game.country)

        key = Key(code=code, account=final_account, game=game)
        key.save()

        final_account.status = True
        final_account.save()
    except:

        account = get_user_by_country("Error")

        key = Key(code=code, account=account, game=game)
        key.save()



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
            for i in get_shops():
                info = api.check_code(code, i.guid, i.seller_id)
                if info['retval'] == 0:
                    if len(Task.objects.filter(task_params__contains=code)) == 0:
                        new_account(info, code)

                    data = {
                        "login": None,
                        "password": None
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


def get_user_by_country(country: str) -> Account:
    return Account.objects.filter(country=country, status=None)[0]


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
        for i in get_shops():
            info = api.check_code(code, i.guid, i.seller_id)
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
                continue

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



def head(request):
    return render(request, 'main/head.html')
