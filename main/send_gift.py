import time
import random
import imaplib
import email
import traceback
import email.header
import re
from aiogram import Bot

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from seleniumwire import webdriver
from selenium.webdriver.support.select import Select

from .models import Account, SteamCode, Game, Telegram

bot = Bot('1977433713:AAESITNZaLacqpTnqBrIkc5GaWD9SrX6NYo')


def get_steam_code(value: int, country: str) -> SteamCode:
    code = SteamCode.objects.filter(country=country, value=value, status=None)[0]
    code.status = False
    code.save()
    return code


def get_telegram():
    final_list = []
    tg_accounts = Telegram.objects.all()
    for tg_account in tg_accounts:
        final_list.append(tg_account.tg_id)
    return final_list


def get_codes_amount(text):
    list_text = text.split(',')
    for i in list_text:
        index = list_text.index(i)
        list_text[index] = int(i.strip(' '))
    return list_text


def steam_login(driver, login: str, password: str, email_login: str, email_password):
    driver.get('http://steamcommunity.com/login/home/?goto=')
    time.sleep(2)
    login_input = driver.find_element_by_xpath('//*[@id="input_username"]')
    for i in login:
        login_input.send_keys(i)
        time.sleep(random.uniform(0, 0.2))
    password_input = driver.find_element_by_xpath('//*[@id="input_password"]')
    for i in password:
        password_input.send_keys(i)
        time.sleep(random.uniform(0, 0.2))
    driver.find_element_by_xpath('//*[@id="login_btn_signin"]/button/span').click()
    time.sleep(5)
    try:
        code_input = driver.find_element_by_xpath('//*[@id="authcode"]')
        if code_input.is_displayed() is False:
            return True
        code = get_code(email_login, email_password)
        if code == 'The code has not arrived yet':
            time.sleep(10)
            code = get_code(email_login, email_password)
        for i in code:
            code_input.send_keys(i)
            time.sleep(random.uniform(0, 0.2))
        driver.find_element_by_xpath('//*[@id="auth_buttonset_entercode"]/div[1]').click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@id="success_continue_btn"]/div[1]').click()
        except ElementNotInteractableException:
            try:
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="success_continue_btn"]/div[1]').click()
            except ElementNotInteractableException:
                code_input = driver.find_element_by_xpath('//*[@id="authcode"]')
                code_input.clear()
                code = get_code(email_login, email_password)
                for i in code:
                    code_input.send_keys(i)
                    time.sleep(random.uniform(0, 0.2))
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="auth_buttonset_incorrectcode"]/div[1]').click()
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="success_continue_btn"]/div[1]').click()
        time.sleep(5)
    except NoSuchElementException:
        time.sleep(5)


def get_code(from_email, from_pwd):
    try:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(from_email)
        print(from_pwd)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        smtp_server = "imap.rambler.ru"
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(from_email, from_pwd)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        latest_email_id = int(id_list[-1])

        data = mail.fetch(str(latest_email_id), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))

                try:
                    # Поиск в теле письма кода для смены email.

                    code = str(re.findall('[0-9-A-Z]{5}[/\n]', str(msg).split("Content-Transfer")[2])[0]).strip('\n')
                    if "UTF" not in code:
                        return code
                    else:
                        return 'The code has not arrived yet'
                except IndexError:
                    try:
                        # Поиск в теле письма кода для входа на новом устройстве.

                        code = str(re.findall('[0-9-A-Z]{5}[/\n]', str(msg).split("Content-Transfer")[2])[0]).strip(
                            '\n')
                        if len(code) > 10:
                            return 'The code has not arrived yet'
                        if "UTF" not in code:
                            return code
                        else:
                            return 'The code has not arrived yet'
                    except IndexError:
                        return 'The code has not arrived yet'
    except Exception as e:
        traceback.print_exc()
        print(str(e))


def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


def buy_game(driver, game_link):
    driver.get(game_link)
    time.sleep(3)
    try:
        select_element = driver.find_element_by_xpath('//*[@id="ageYear"]')
        time.sleep(0.5)
        Select(select_element).select_by_value('2002')
        driver.find_element_by_xpath('//*[@id="app_agegate"]/div[1]/div[4]/a[1]/span').click()
        time.sleep(1)
    except NoSuchElementException:
        pass
    # Добавить в корзину
    try:
        driver.find_element_by_xpath("//*[contains(@href,'addToCart')]").click()
    except:
        driver.find_element_by_xpath("//*[contains(@href,'addBundleToCart')]").click()

    # Купить для себя
    driver.find_element_by_xpath('//*[@id="btn_purchase_self"]/span').click()
    time.sleep(1)
    # Потверждаем покупку
    try:
        driver.find_element_by_xpath('//*[@id="accept_ssa"]').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="purchase_button_bottom_text"]').click()
        time.sleep(3)
    except NoSuchElementException:
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="accept_ssa"]').click()
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="purchase_button_bottom_text"]').click()
        time.sleep(3)


def full_send(account: Account, game: Game, game_link: str, country: str):
    tg_list = get_telegram()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    need_codes = get_codes_amount(game.codes)

    try:
        steam_login(driver, account.steam_login, account.steam_password, account.email, account.email_password)
        time.sleep(5)
    except Exception as e:
        print(e)
        for tg_id in tg_list:
            try:
                bot.send_message(tg_id, 'Ошибка входа!')
            except Exception as e:
                print(e)
        driver.quit()


    for i in need_codes:

        try:
            code = get_steam_code(i, country)
        except Exception as e:
            print(e)
            for tg_id in tg_list:
                try:
                    bot.send_message(tg_id, f'Недостаток кодов! Номинал {i}. Страна - {country}')
                except Exception as e:
                    print(e)
            driver.quit()

        code.account = account
        code.save()
        driver.get('https://store.steampowered.com/account/redeemwalletcode')
        driver.find_element_by_xpath('//*[@id="wallet_code"]').send_keys(code.code)
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="validate_btn"]/span').click()
        time.sleep(5)
        if driver.find_element_by_xpath('//*[@id="redeem_wallet_success_button_text"]').is_displayed():
            code.status = True
            code.save()
        else:
            time.sleep(15)
            code.status = True
            code.save()

    time.sleep(3)

    try:
        buy_game(driver, game_link)
    except Exception as e:
        print(e)
        for tg_id in tg_list:
            try:
                bot.send_message(tg_id, f'Не удалось купить! Игра - {game.name}')
            except Exception as e:
                print(e)
        driver.quit()
    driver.quit()

    return account
