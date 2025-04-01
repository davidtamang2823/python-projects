from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    dob = models.DateField()
    user_profile_pic = models.FileField(upload_to='user_profile_images/',null=True, blank=True, default='user_profile_images/default.PNG')

    

class Destination(models.Model):

    ZIP_CODE = (
        (44600, "44600 Kathmandu"),
        (44800, "44800 Bhaktapur"),
        (44200, "44200 Chitwan"),
        (32900, "32900 Bhairahawa"),
        (33700, "33700 Pokhara")
    )

    destination_name = models.CharField(max_length=30, blank=False, null=False,unique = True)
    zip_code = models.IntegerField(choices = ZIP_CODE, unique = True, default=True)
    destination_pic = models.ImageField(upload_to='destination_pic/' ,null=False, blank=False)
    destination_description = models.TextField(blank=False, null = False, default=True)
    def __str__(self):
        return self.destination_name
    

class Location(models.Model):
    address_name = models.CharField(max_length=150, null=False, blank=False)
    address_info = models.TextField(blank=False, null=False,default=True)
    def __str__(self):
        return self.address_name

class HotelType(models.Model):
    hotel_type_names = models.CharField(max_length=100, null=False, blank=False ,unique = True)
    hotel_type_description = models.TextField(blank=False)
    def __str__(self):
        return self.hotel_type_names


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=150, null=False, blank = False, unique = True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE ,null=False, blank=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,null=False, blank = False)
    hotel_rating = models.IntegerField(null=False, blank=False, default = 0)
    hotel_description = models.TextField(null = False, blank = False)
    hotel_pic = models.ImageField(upload_to='hotel_images/', blank = False, null = False)
    hotel_type = models.ForeignKey(HotelType, on_delete=models.CASCADE, null=False, blank=False,default=True)
    def __str__(self):
        return self.hotel_name


class RoomType(models.Model):
    room_type_names = models.CharField(max_length=200, null=False, blank = False, unique = True)
    room_type_description = models.TextField(blank = False, null = False)

    def __str__(self):
        return self.room_type_names

class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null = False, blank=False)
    room_number = models.IntegerField(blank=False, null = False)
    room_type = models.ForeignKey(RoomType,on_delete=models.CASCADE, blank = False)
    room_rent_price = models.IntegerField(blank=False)
    total_capacity_of_child_guest = models.IntegerField(blank=False,  default=0)
    total_capacity_of_adult_guest = models.IntegerField(blank=False, default=1)
    isBooked = models.BooleanField(default = False)
    def __str__(self):
        return f'{self.hotel.hotel_name} {self.room_number} {self.room_type.room_type_names}'
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = False)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null = False)
    booking_date = models.DateTimeField(default=datetime.now(), null=False)
    check_in_date_time = models.DateTimeField(null=False, default=None)
    check_out_date_time = models.DateTimeField(null = False, default=None)
    number_of_adult_guest = models.IntegerField(default=1, null=False)
    number_of_child_guest = models.IntegerField(default=0, null=False)
    isCanceled = models.BooleanField(null=False, default=False)
    isBookingExpired = models.BooleanField(null=False, default=False)
    isChecked_in = models.BooleanField(null=False, blank=False, default=False)

class BookingHistory(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = False)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null = False)
    booking_date = models.DateTimeField(default=datetime.now(), null=False)
    check_in_date_time = models.DateTimeField(null=False, default=None)
    check_out_date_time = models.DateTimeField(null = False, default=None)
    number_of_adult_guest = models.IntegerField(default=1, null=False)
    number_of_child_guest = models.IntegerField(default=0, null=False)
    isCanceled = models.BooleanField(null=False, default=False)
    isBookingExpired = models.BooleanField(null=False, default=False)
    isChecked_in = models.BooleanField(null=False, blank=False, default=False)


class HotelBookingHour(models.Model):
    BOOKING_CHECK_IN_HOURS = []
    BOOKING_CHECK_OUT_HOURS = []   

    for x in range(1,13):
        hour = (f'{x}:00:00',f'{x}:00:00')
        half_hour = (f'{x}:30:00',f'{x}:30:00')

        BOOKING_CHECK_IN_HOURS.append(hour)
        BOOKING_CHECK_IN_HOURS.append(half_hour)

        BOOKING_CHECK_OUT_HOURS.append(hour)
        BOOKING_CHECK_OUT_HOURS.append(half_hour)

    for x in range(13,24):
        hour = (f'{x}:00:00',f'{x}:00:00')
        half_hour = (f'{x}:30:00',f'{x}:30:00')

        BOOKING_CHECK_IN_HOURS.append(hour)
        BOOKING_CHECK_IN_HOURS.append(half_hour)

        BOOKING_CHECK_OUT_HOURS.append(hour)
        BOOKING_CHECK_OUT_HOURS.append(half_hour)

    hour = (f'00:00:00',f'00:00:00')
    half_hour = (f'00:30:00',f'00:30:00')
    BOOKING_CHECK_IN_HOURS.append(hour)
    BOOKING_CHECK_IN_HOURS.append(half_hour)
    BOOKING_CHECK_OUT_HOURS.append(hour)
    BOOKING_CHECK_OUT_HOURS.append(half_hour)

    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE, blank=False, null=False)
    hotel_check_in_hour = models.CharField(max_length=40,choices=BOOKING_CHECK_IN_HOURS, blank=False, null=False)
    hotel_check_out_hour = models.CharField(max_length=40,choices=BOOKING_CHECK_OUT_HOURS, blank=False, null=False)

    def __str__(self):
        return f'{self.hotel.hotel_name} Check-in {self.hotel_check_in_hour} Check-out {self.hotel_check_out_hour}'


class RoomAmenities(models.Model):
    amenities_name = models.CharField(max_length=100 ,null=False, blank=False,unique = True)
    amenities_description = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.amenities_name


class HotelRoomAmenities(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null = False)
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null = False)
    room_amenities = models.ForeignKey(RoomAmenities, on_delete=models.CASCADE, null = False)
    def __str__(self):
        return f'{self.hotel.hotel_name} {self.hotel_room.room_number} {self.room_amenities.amenities_name}'
    
    

"""
class HotelReview(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False, blank = False)
    given_rating = models.IntegerField(max = 5, null = False, blank = False)
    comment = models.TextField(null=True, blank = True)
    created_date = models.DateField(auto_now_add=True)
    edited = models.BooleanField()
    """