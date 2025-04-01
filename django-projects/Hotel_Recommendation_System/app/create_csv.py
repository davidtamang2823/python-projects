import csv
from app.models import *
import os.path

# """
# Hotel_details.csv

# hotelid
# hotelname
# hoteltype
# destination

# Hotel_Room_attributes.csv

# hotelid
# roomamenities
# roomtype

# """

def create_file():
   
    if os.path.isfile('Hotel_details.csv') == False:
        
        hotel_lists = [['hotelid','hotelname','hoteltype','destination']]
        get_all_hotels = Hotel.objects.all()
        for h in get_all_hotels:
            hotel_lists.append([h.id, h.hotel_name, h.hotel_type.hotel_type_names, h.destination.destination_name])
        
        with open('Hotel_details.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(hotel_lists)

    if os.path.isfile('Hotel_Room_attributes.csv') == False:
        
        hotel_room_lists = [['hotelid', 'roomamenities', 'roomtype']]
        get_hotel_rooms = HotelRoom.objects.all()
        
        for r in get_hotel_rooms:
            amenities = ''
            get_room_amenities = HotelRoomAmenities.objects.filter(hotel=r.hotel, hotel_room = r.id)
            for a in get_room_amenities:
                amenities = amenities + a.room_amenities.amenities_name + ', '
            hotel_room_lists.append([r.hotel.id, amenities.strip(),  r.room_type.room_type_names])

        with open('Hotel_Room_attributes.csv','w') as file:
            writer = csv.writer(file)
            writer.writerows(hotel_room_lists)
    
    
    else:
        print('File exists')

