# Generated by Django 5.0.6 on 2024-06-16 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("telegram", "0004_alter_business_options_cklient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userbusiness",
            name="referrer_id",
            field=models.CharField(
                default=1, max_length=100, verbose_name="Айди реферальки"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="userbusiness",
            name="user_id",
            field=models.CharField(max_length=100, verbose_name="Айди"),
        ),
        migrations.AlterField(
            model_name="userbusiness",
            name="username",
            field=models.CharField(
                default=11, max_length=100, verbose_name="Имя пользователя"
            ),
            preserve_default=False,
        ),
    ]
