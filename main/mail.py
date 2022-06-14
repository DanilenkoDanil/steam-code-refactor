import imaplib
import email
import traceback
import email.header
import re
from main.models import Account


# Расшифровка письма.
def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


def get_user_by_login(login: str):
    return Account.objects.filter(steam_login=login)[0]


# Эта функция сканирует ПОСЛЕДНЕЕ полученное письмо на наличие кода и возвращает КОД.
# Чтобы поменять сервис достаточно заменить smtp_server на нужный. Сейчас работает с rambler.
# ОБЯЗАТЕЛЬНО разрешите подключение сторонних приложений к аккаунту в настройка почты!
def get_code(account: Account):
    try:
        from_email = account.email
        from_pwd = account.email_password
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

                        code = str(re.findall('[0-9-A-Z]{5}[/\n]', str(msg).split("Content-Transfer")[2])[0]).strip('\n')
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


# Небольшой тест
if __name__ == '__main__':

    print(get_code('songregasan1972@rambler.ru', 'MdpHWvGwKz1998'))
