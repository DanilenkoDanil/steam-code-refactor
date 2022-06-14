from django.db import models


class Account(models.Model):
    steam_login = models.TextField(
        verbose_name="Логин пользователя в Steam",
        unique=True
    )
    steam_password = models.TextField(
        verbose_name="Пароль от Steam"
    )
    email = models.TextField(
        verbose_name='Почта к которой привязан аккаунт'
    )
    email_password = models.TextField(
        verbose_name='Пароль от почты'
    )
    status = models.BooleanField(
        verbose_name='Статус аккаунта',
        null=True,
    )
    country = models.TextField(
        verbose_name='Страна'
    )

    def __str__(self):
        return f'#{self.steam_login}'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class SteamCode(models.Model):
    code = models.TextField(
        verbose_name="Код",
        unique=True
    )
    value = models.PositiveIntegerField(
        verbose_name="Сумма",
    )
    country = models.TextField(
        verbose_name='Страна'
    )

    status = models.BooleanField(
        verbose_name='Статус',
        null=True,
    )
    account = models.ForeignKey(
        to='main.Account',
        verbose_name='Аккаунт',
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'#{self.code}'

    class Meta:
        verbose_name = 'Код пополнения'
        verbose_name_plural = 'Коды пополнения'


class Game(models.Model):
    sell_code = models.PositiveIntegerField(
        verbose_name='Код продажи'
    )
    name = models.TextField(
        verbose_name='Название игры'
    )
    app_code = models.PositiveIntegerField(
        verbose_name='Код игры в стиме'
    )
    country = models.TextField(
        verbose_name='Страна'
    )
    codes = models.TextField(
        verbose_name='Карты'
    )

    def __str__(self):
        return f'{self.sell_code} - {self.name}'

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = 'Игры'


class Key(models.Model):
    code = models.TextField(
        verbose_name='Код покупки',
        unique=True
    )
    game = models.ForeignKey(
        to='main.Game',
        verbose_name='Игра',
        on_delete=models.PROTECT,
    )
    account = models.ForeignKey(
        to='main.Account',
        verbose_name='Аккаунт',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f'Ключ - {self.code}'

    class Meta:
        verbose_name = "Ключ"
        verbose_name_plural = 'Ключи'


class Telegram(models.Model):
    tg_id = models.TextField(
        verbose_name='ID Аккаунта',
        unique=True
    )
    name = models.TextField(
        verbose_name='Имя',
    )

    def __str__(self):
        return f'Аккаунт - {self.id} - {self.name}'

    class Meta:
        verbose_name = "Телеграм"
        verbose_name_plural = 'Телеграм'


class Shop(models.Model):
    name = models.TextField(
        verbose_name='Название магазина',
    )
    guid = models.TextField(
        verbose_name='API Guid',
    )
    seller_id = models.TextField(
        verbose_name='Seller ID'
    )

    def __str__(self):
        return f'Магазин - {self.name}'

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = 'Магазины'
