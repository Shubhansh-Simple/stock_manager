# Generated by Django 2.2 on 2021-03-01 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_app', '0002_remove_icecream_freezer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='total',
            name='last_update',
        ),
    ]
