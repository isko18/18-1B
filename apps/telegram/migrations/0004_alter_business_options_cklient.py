# Generated by Django 5.0.6 on 2024-06-16 19:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("telegram", "0003_usercklient_userbusiness_username"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="business",
            options={"verbose_name_plural": "Отели Бизнесов"},
        ),
        migrations.CreateModel(
            name="Cklient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("region", models.CharField(max_length=155, verbose_name="Район")),
                ("date", models.CharField(max_length=155, verbose_name="Дата Заезда")),
                ("comment", models.TextField(verbose_name="Комментраия")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="telegram.usercklient",
                        verbose_name="Пользователи",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Бронирование Клиента",
            },
        ),
    ]
