from app.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse


def api_user_booking_details(request, un):
    try:
        user = User.objects.get(username =un)
        user_booking_lists = {}
        get_user_bookings = BookingHistory.objects.filter(user=user)

        for b in range(len(get_user_bookings)):

            ub = get_user_bookings[b]
            i = str(b)
            if 'userid' not in user_booking_lists and 'hotelid' not in user_booking_lists and 'hoteltype' not in user_booking_lists and 'roomtype' not in user_booking_lists:
                user_booking_lists['userid'] = {i:ub.user.id}
                user_booking_lists['hotelid'] = {i:ub.room.hotel.id}
                user_booking_lists['hoteltype'] = {i:ub.room.hotel.hotel_type.hotel_type_names}
                user_booking_lists['roomtype'] = {i:ub.room.room_type.room_type_names}

            else:
                user_booking_lists['userid'][i] = ub.user.id
                user_booking_lists['hotelid'][i] = ub.room.hotel.id
                user_booking_lists['hoteltype'][i] = ub.room.hotel.hotel_type.hotel_type_names
                user_booking_lists['roomtype'][i] = ub.room.room_type.room_type_names

        if len(user_booking_lists.values()) > 0:
            return JsonResponse(user_booking_lists, safe=False)
        else:
            return JsonResponse({'userid':{}, 'hotelid':{}, 'hoteltype':{}, 'roomtype':{}})
    except:
        return JsonResponse({'Error':'No data found'})