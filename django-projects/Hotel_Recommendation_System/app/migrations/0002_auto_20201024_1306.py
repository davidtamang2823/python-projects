# Generated by Django 3.1.1 on 2020-10-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='user_profile_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
