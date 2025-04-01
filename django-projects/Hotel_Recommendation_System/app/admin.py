from django.contrib import admin
from app.models import Destination, Location, Hotel, HotelType, RoomType, RoomAmenities, HotelRoom, HotelRoomAmenities, HotelBookingHour, Booking
# Register your models here.
admin.site.register(Destination)
admin.site.register(Location)
admin.site.register(HotelType)
admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(RoomAmenities)
admin.site.register(HotelRoom)
admin.site.register(HotelRoomAmenities)
admin.site.register(HotelBookingHour)
admin.site.register(Booking)

