# Generated by Django 5.0.6 on 2024-06-17 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0005_alter_userbusiness_referrer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cklient',
            name='comment',
            field=models.TextField(verbose_name='Комментарий'),
        ),
    ]
