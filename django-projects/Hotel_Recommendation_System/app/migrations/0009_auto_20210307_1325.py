# Generated by Django 3.1.5 on 2021-03-07 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_auto_20210207_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField()),
                ('isBooked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
                ('room_rent_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoomAmenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('hotel_room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotelroom')),
            ],
        ),
        migrations.CreateModel(
            name='HotelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_type_names', models.CharField(max_length=100, unique=True)),
                ('hotel_type_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomAmenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenities_name', models.CharField(max_length=100, unique=True)),
                ('amenities_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type_names', models.CharField(max_length=200, unique=True)),
                ('room_type_description', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_rent',
        ),
        migrations.AddField(
            model_name='destination',
            name='destination_description',
            field=models.TextField(default=True),
        ),
        migrations.AddField(
            model_name='destination',
            name='zip_code',
            field=models.CharField(choices=[(44600, '44600 Kathmandu'), (44800, '44800 Bhaktapur'), (44200, '44200 Chitwan')], default=True, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='location',
            name='address_info',
            field=models.TextField(default=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='destination_name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='hotel_name',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='location',
            field=models.CharField(max_length=300),
        ),
        migrations.AddField(
            model_name='hotelroomamenities',
            name='room_amenities_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.roomamenities'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='hotel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotel'),
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='room_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.roomtype'),
        ),
        migrations.AddField(
            model_name='booking',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotelroom'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_type',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='app.hoteltype'),
        ),
    ]
