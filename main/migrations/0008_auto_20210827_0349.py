# Generated by Django 3.2.4 on 2021-08-27 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210826_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='steamcode',
            options={'verbose_name': 'Код пополнения', 'verbose_name_plural': 'Коды пополнения'},
        ),
        migrations.AddField(
            model_name='game',
            name='codes',
            field=models.TextField(default=0, verbose_name='Карты'),
            preserve_default=False,
        ),
    ]
