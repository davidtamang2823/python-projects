# Generated by Django 3.1.5 on 2021-03-15 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20210314_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='no_of_room_booked',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 15, 14, 10, 16, 88151)),
        ),
    ]
