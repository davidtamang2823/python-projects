# Generated by Django 3.1.1 on 2020-11-03 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201027_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.TextField(max_length=30)),
                ('location_pic', models.FileField(upload_to='location_pic/')),
            ],
        ),
    ]
