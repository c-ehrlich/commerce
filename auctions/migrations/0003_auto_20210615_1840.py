# Generated by Django 3.2.4 on 2021-06-15 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_auction_ending_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='auction',
            name='ending_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 22, 18, 40, 40, 515180)),
        ),
    ]
