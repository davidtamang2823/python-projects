# Generated by Django 3.1.5 on 2021-03-12 06:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20210312_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='isBooked',
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='isBooked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 12, 12, 18, 52, 794095)),
        ),
    ]
