# Generated by Django 5.0.1 on 2024-03-28 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpr', '0020_onlineauctionbidtable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlineauctionbidtable',
            name='utype',
        ),
    ]
