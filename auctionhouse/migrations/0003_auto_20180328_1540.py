# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-28 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionhouse', '0002_auto_20180328_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
    ]
