from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse, reverse
from django.contrib.auth.models import User
from app.models import UserDetails, Destination, Hotel, HotelType,HotelRoom, Booking, RoomType, HotelBookingHour, HotelRoomAmenities, BookingHistory
from app.form import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from functools import wraps
from datetime import datetime, timedelta
import datetime as dt
from django.db.models import Q
from recommender import *
import math

# Create your views here.

# all_urls = ['/home/','/signup/','/login/','/logout/']

IMG_EXTENSION = ['jpeg', 'jpg', 'png']

def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_pic = UserDetails.objects.get(user=request.user.id)
            print(user_pic.user_profile_pic)
            get_all_destination = Destination.objects.all()
            context = { 'destination': get_all_destination, 'profile':user_pic}
            return render(request, 'app/index.html', context)
        else:
            get_all_destination = Destination.objects.all()
            context = { 'destination': get_all_destination}
            return render(request, 'app/index.html', context)

    if request.method == 'POST':
        src = request.POST['location-search']
        searched = Destination.objects.filter(destination_name = src.capitalize())
        if searched.count() > 0:
            context = { 'src': searched}
            return render(request, 'app/index.html', context)


    

def sign_up(request):
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
       
        if form.is_valid():
            un  = form.cleaned_data['username']
            em  = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            fn  = form.cleaned_data['first_name']
            ln  = form.cleaned_data['last_name']
            dob = form.cleaned_data['dob']
            img = form.cleaned_data['user_img']
            
            User.objects.create_user(username = un, email = em, password = pwd,
            first_name = fn, last_name = ln)

            getUser = User.objects.get(username = un)
            if img is not None:
                UserDetails.objects.create(user_id = getUser.id, dob = dob,  user_profile_pic= img)
            else:
                UserDetails.objects.create(user_id = getUser.id, dob = dob)
            
            messages.add_message(request, messages.SUCCESS, 'Please login with your new username and password.')
            return HttpResponseRedirect('/login/')
        
    return render(request, 'app/SignUp.html',{'fields':form})
            

def user_login(request):
    if request.method == 'GET':
        print(request.path)
        return render(request, 'app/login.html')
    else:
        un = request.POST['username']
        pwd = request.POST['password']

        user = authenticate(username = un, password = pwd)

        if user is not None:    
            login(request, user)
            return HttpResponseRedirect(reverse(home))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password' )
            return HttpResponseRedirect('/login/')
            

# def forgot_password(request):
#     if request.method == 'GET':
#         return render(request, 'app/ForgotPassword.html')
#     else:
#         return HttpResponse('forgot password post request is still in progress')





@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(home))


#def find_hotels(request):

    


#Restrict page after user logged in
def filter_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(home))
    else:
        if request.path == '/login/':
            return user_login(request)
        elif request.path == '/signup/':
            return sign_up(request)
            
        


def is_valid_file(fileName):
    fn = fileName.split('.')
    if fn[1].lower() in IMG_EXTENSION:
        return True
    else:
        return False

def edit_user(id , fn, ln):
    user = User.objects.get(id = id)
    user.first_name = fn
    user.last_name = ln
    user.save()

@login_required(login_url='/login/')
def user_profile(request):
    if request.method == 'GET':
        ud = UserDetails.objects.get(user_id = request.user.id)
        # user_pic = UserDetails.objects.get(user=request)
        return render(request, 'app/profile.html',{'ud':ud})
    else:
        fn = request.POST['first_name']
        ln = request.POST['last_name']
        
        try:
            pimg = request.FILES['edit_pic']
        except:
            pimg = None
        finally:
            id = request.user.id
            if pimg is not None:
                if is_valid_file(pimg.name) and pimg is not None:

                    edit_user(id, fn, ln)
                    ud = UserDetails.objects.get( user =id)
                    ud.user_profile_pic = pimg
                    ud.save()
                
                    return render(request, 'app/profile.html',{'ud':ud})
            
            elif pimg is None:
                edit_user(id, fn, ln)
                ud = UserDetails.objects.get(user = id)
                return render(request, 'app/profile.html',{'ud':ud})

            else:
                messages.add_message(request, messages.ERROR, 'You should upload image file')
                ud = UserDetails.objects.get(user = request.user.id)
                return render(request, 'app/profile.html',{'ud':ud})


def view_hotels(request, destination):
    if request.method == 'GET':

        get_destination = Destination.objects.get(destination_name=destination)
        get_destination_id = get_destination.id
        get_destination_name = destination

        hotels = Hotel.objects.filter(destination=get_destination_id)
        total_pages = math.ceil(hotels.count() / 10)
        get_pages = [ x+1 for x in range(total_pages)]
        get_hotels = hotels[0:10]

        if request.user.is_authenticated:
            recommendation_lists = create_recommendation_list(request.user.username, destination)
            
            if recommendation_lists is not None:
                context = {'destination_name':get_destination_name, 
                'hotels':get_hotels, 
                'recommendation_lists':recommendation_lists,
                'pages':get_pages}
            
                return render(request, 'app/hotels.html', context)
            else:
                best_hotels = Hotel.objects.all().order_by('-hotel_rating')[:5]
                context = {'destination_name':get_destination_name, 
                'hotels':get_hotels, 
                'pages':get_pages,
                'best_hotels': best_hotels}
            
                return render(request, 'app/hotels.html', context)
        else:
            best_hotels = Hotel.objects.all().order_by('-hotel_rating')[:5]
            context = {'destination_name':get_destination_name, 
            'hotels':get_hotels, 
            'pages':get_pages,
            'best_hotels': best_hotels}
        
            return render(request, 'app/hotels.html', context)



def start(pageNo):
    start_no = (pageNo - 1) * 10
    return start_no

def end(pageNo):
    end_no = pageNo * 10
    return end_no


def view_hotels_by_page(request, destination, pageNo):
    if request.method == 'GET':

        get_destination = Destination.objects.get(destination_name=destination)
        get_destination_id = get_destination.id
        get_destination_name = destination

        hotels = Hotel.objects.filter(destination=get_destination_id)
        total_pages = math.ceil(hotels.count()/10)
        get_pages = [ x+1 for x in range(total_pages)]
        get_hotels = hotels[start(pageNo):end(pageNo)]


        if request.user.is_authenticated:
            recommendation_lists = create_recommendation_list(request.user.username, destination)
            if recommendation_lists is not None:

                context = {'destination_name':get_destination_name, 
                'hotels':get_hotels, 
                'recommendation_lists':recommendation_lists,
                'pages':get_pages,
                'pageNo':pageNo}

                return render(request, 'app/hotels.html', context)
            else:
                best_hotels = Hotel.objects.all().order_by('-hotel_rating')[:5]
                context = {'destination_name':get_destination_name, 
                'hotels':get_hotels, 
                'pages':get_pages,
                'best_hotels': best_hotels}
                
                return render(request, 'app/hotels.html', context)
        else:
            best_hotels = Hotel.objects.all().order_by('-hotel_rating')[:5]
            context = {'destination_name':get_destination_name, 
            'hotels':get_hotels, 
            'pages':get_pages,
            'best_hotels': best_hotels}
            
            return render(request, 'app/hotels.html', context)



#Booking

def date_to_datetime(date, time):
   
    split_date = date.split('-')

    year = split_date[0]
    month = split_date[1]
    day = split_date[2]

    split_time = time.split(':')

    hour = split_time[0]
    minute = split_time[1]
    second = split_time[2]

    date_time = f'{day}/{month}/{year} {hour}:{minute}:{second}'

    datetime_obj = datetime.strptime(date_time, f'%d/%m/%Y %H:%M:%S')

    return datetime_obj


def is_valid_no_of_guests(hotel_id, room_type_name, no_of_guests):
    get_room_type_id =  RoomType.objects.get(room_type_names=room_type_name).id

    get_room = HotelRoom.objects.filter(hotel=hotel_id, room_type_id = get_room_type_id)[0]
    get_child_no = get_room.total_capacity_of_child_guest
    get_adult_no = get_room.total_capacity_of_adult_guest

    for adult_guest, child_guest in no_of_guests.values():

        if adult_guest < 1 or adult_guest > get_adult_no or child_guest > get_child_no:
            return False
    
    return True


def check_room_availability(hotel_id, room_type_name, check_in_date_time, check_out_date_time):

    get_room_type_id = RoomType.objects.get(room_type_names=room_type_name)
    get_rooms = HotelRoom.objects.filter( hotel = hotel_id, room_type=get_room_type_id )
    

    for room in get_rooms:

        
        get_bookings = Booking.objects.filter(room_id = room.id).order_by('check_out_date_time')

        if not bool(room.isBooked):
            return room
        else:
            new_book = None
            for b in get_bookings:
                #check wheather a room in booked on check_in_date or not
                if b.check_in_date_time.date() == check_in_date_time.date():
                    print(b.check_in_date_time.date(),'======> 1',check_in_date_time.date())
                    new_book = None
                    break
                
                #check wheather check_out date is greater than check_in_date
                elif b.check_out_date_time.date() > check_in_date_time.date():
                    print(b.check_in_date_time.date(),'======> 2',check_in_date_time.date())
                    new_book = None
                    break    

                #check wheather same day check out time is greater than check in time or not
                elif b.check_out_date_time.date() == check_in_date_time.date() and b.check_out_date_time.time() > check_in_date_time.time():
                    print(b.check_in_date_time.date(),'======> 3',check_in_date_time.date())
                    new_book = None
                    break
                
                #check wheather same day but other day book or not
                elif  b.check_in_date_time.date() > check_in_date_time.date() and check_out_date_time.date() > b.check_in_date_time.date():
                    print(b.check_in_date_time.date(),'======> 4',check_in_date_time.date())
                    new_book = None
                    break


                elif b.check_out_date_time.date() <= check_in_date_time.date() and b.check_out_date_time.time() <= check_in_date_time.time():
                    new_book = room
                    
                    # return new_book
                    
            if new_book is not None:
                return new_book


    return None


def is_valid_date(check_in_datetime, check_out_datetime):
    current_datetime = datetime.now()

    if check_in_datetime.date == current_datetime.date:
        if check_in_datetime.time() < current_datetime.time():
            return False

    elif check_in_datetime.date() == check_out_datetime.date():
        return False

    elif check_in_datetime < current_datetime:
        return False

    return True

def get_room_amenities(hotel_id):

    room_amenities = {}
    get_room_amenities = HotelRoomAmenities.objects.filter(hotel = hotel_id)
    already = []
    for a in get_room_amenities:
       get_amenities = HotelRoomAmenities.objects.filter(hotel = hotel_id, hotel_room=a.hotel_room)
       for g in get_amenities:
           if g.hotel_room.room_type.room_type_names not in already:
              if g.hotel_room.room_type.room_type_names not in room_amenities:
                  room_amenities[g.hotel_room.room_type.room_type_names] = []
                  room_amenities[g.hotel_room.room_type.room_type_names].append(g.room_amenities.amenities_name)
              else:
                  room_amenities[g.hotel_room.room_type.room_type_names].append(g.room_amenities.amenities_name)
           else:
                break
       already.append(a.hotel_room.room_type.room_type_names)
    return room_amenities


def get_guests_number(hotel_id):
    hotel_rooms = HotelRoom.objects.filter(hotel_id = hotel_id)
    print(hotel_rooms)
    booking_rooms_no = {}
   
    for r in hotel_rooms:
        rt = r.room_type.room_type_names
        if  rt not in booking_rooms_no:
            booking_rooms_no[rt] = []
            booking_rooms_no[rt].append(1)
        else:
            sum = booking_rooms_no[rt][-1] + 1
            booking_rooms_no[rt].append(sum)

    print(booking_rooms_no)
    return booking_rooms_no


def room_available_no(room_id, check_in_date_time, check_out_date_time):
    get_rooms = HotelRoom.objects.filter(room = room_id)
    room_available = 0

def is_user_booked(user_id):
    is_booked = Booking.objects.get(user=user_id)
    if is_booked is None:
        return False
    else:
        return True

        
def get_unique_room(hid):
    rid = HotelRoom.objects.filter(hotel_id = hid).order_by().values('room_type').distinct()
    empty_list = []
    for x in rid:
        empty_list.append(HotelRoom.objects.filter(hotel=hid, room_type = x['room_type'])[0])
    return empty_list

@login_required(login_url='/login/')
def book_hotel(request, destination, hotel_name, id):

    get_hotel = Hotel.objects.get(id = id)
    get_room = get_unique_room(id)
    get_hotel_booking_hours = HotelBookingHour.objects.filter(hotel = id)
    room_amenities = get_room_amenities(id)
    current_date = datetime.now().date()
    booking_rooms_no = get_guests_number(id)
      
    user_booking = Booking.objects.filter(user = request.user.id)
    isBooked = False
    isCurrentBooking = False
    if user_booking.count() > 0:
        isBooked = True
        if user_booking[0].room.hotel.id == id:
            isCurrentBooking = True

    if request.method == 'GET':

        context = {'hotel':get_hotel, 
        'room':get_room,
        'booking_hours':get_hotel_booking_hours,
        'amenities':room_amenities,
        'brn':booking_rooms_no,
        'isBooked':isBooked,
        'isCurrentBooking':isCurrentBooking
        }

        return render(request, 'app/booking.html', context)

    if request.method == 'POST':
        if not isBooked:
            check_in_date = request.POST['check-in-date']
        
            check_out_date = request.POST['check-out-date']
            
            booking_hour = int(request.POST['booking-hour'])

            get_booking_hour = HotelBookingHour.objects.get(id = booking_hour)

            #required variable for booking module
            check_in_date_time = date_to_datetime(check_in_date, get_booking_hour.hotel_check_in_hour)
            check_out_date_time = date_to_datetime(check_out_date, get_booking_hour.hotel_check_out_hour)

            no_of_room_booked  = {}
            no_of_guests = {}

            for b in get_guests_number(id).keys():
                no_of_room_booked[b] = int(request.POST[b])
            

            for a,b in no_of_room_booked.items():

                if b > 0:
                    for g in range(1, b+1):
                        k1 = int(request.POST[f'{a} {g} adult'])
                        k2 = int(request.POST[f'{a} {g} child'])

                        if a not in no_of_guests:
                            no_of_guests[a] = {f'room {g}':(k1, k2)}
                        else:
                            no_of_guests[a][f'room {g}'] = (k1, k2)
            
            print(no_of_guests)

            if is_valid_date(check_in_date_time, check_out_date_time):
                room_to_be_booked = []
                #check each room contains valid range of guests or not
                for r in no_of_guests.keys():
                    if not is_valid_no_of_guests(id, r, no_of_guests[r]):
                        context = {'hotel':get_hotel, 
                        'room':get_room,
                        'booking_hours':get_hotel_booking_hours,
                        'amenities':room_amenities,
                        'brn':booking_rooms_no
                        }
                        messages.add_message(request, messages.ERROR, 'Please enter valid guest for a room.')
                        return render(request, 'app/booking.html', context)

                        # return HttpResponse('Room is not valid')
                
                for a,b in no_of_room_booked.items():
                    if b > 0:
                        for x in range(b):
                            room = check_room_availability(id, a, check_in_date_time, check_out_date_time)
                            if room is not None:
                                room_to_be_booked.append({'id':room, 'guests':no_of_guests[a][f'room {x + 1}']})
                            else:
                                context = {'hotel':get_hotel, 
                                'room':get_room,
                                'booking_hours':get_hotel_booking_hours,
                                'amenities':room_amenities,
                                'brn':booking_rooms_no
                                }
                                messages.add_message(request, messages.ERROR, 'Sorry there are no rooms available.')
                                return render(request, 'app/booking.html', context)

                for b in range(len(room_to_be_booked)):
                    cdt = datetime.now()
                    get_r = HotelRoom.objects.get(id = room_to_be_booked[b]['id'].id)

                    Booking.objects.create(
                    user = request.user, 
                    room = get_r, 
                    check_in_date_time=check_in_date_time,
                    check_out_date_time=check_out_date_time,
                    number_of_adult_guest= room_to_be_booked[b]['guests'][0],
                    number_of_child_guest= room_to_be_booked[b]['guests'][1],
                    booking_date=cdt)

                    BookingHistory.objects.create(
                    user = request.user, 
                    room = get_r, 
                    check_in_date_time=check_in_date_time,
                    check_out_date_time=check_out_date_time,
                    number_of_adult_guest= room_to_be_booked[b]['guests'][0],
                    number_of_child_guest= room_to_be_booked[b]['guests'][1],
                    booking_date=cdt)
                    
                    get_r.isBooked = True
                    get_r.save()

                return redirect(f'/{destination}/{hotel_name}/{id}')

            else:
                context = {'hotel':get_hotel, 
                    'room':get_room,
                    'booking_hours':get_hotel_booking_hours,
                    'amenities':room_amenities,
                    'brn':booking_rooms_no
                    }
                messages.add_message(request, messages.ERROR, 'Hotel booking should be from today(current time) or tomorrow.')
                return render(request, 'app/booking.html', context)
        else:
            
            return redirect(f'/{destination}/{hotel_name}/{id}')
    # return HttpResponse('Nothing')

def make_is_book_false(r_id):
    r = HotelRoom.objects.get(id = r_id)
    r.isBookingExpired = True
    r.save()

def remove_booking_data():
    current_datetime = datetime.now()
    booking_details = Booking.objects.all()

    for b in booking_details:
        if b.check_out_date_time.date() < current_datetime.date():
            count_r = Booking.objects.filter(room = b.room.id).count()
            if count_r == 1:
                make_is_book_false(b.room.id)

            b.delete()
        
        elif b.check_out_date_time.date() == current_datetime.date() and b.check_out_date_time.time() <= current_datetime.time():
            count_r = Booking.objects.filter(room = b.room).count()
            if count_r == 1:
                make_is_book_false(b.room.id)

            b.delete()




def check_booking_expired():
    current_datetime = datetime.now()
    booking_details = BookingHistory.objects.filter(isChecked_in=False)

    for b in booking_details:

        if current_datetime.date() > b.check_out_date_time.date():
            b.isBookingExpired = True
            b.save()
            
        
        elif b.check_out_date_time.date() == current_datetime.date() and b.check_out_date_time.time() <= current_datetime.time():
            b.isBookingExpired = True
            b.save()


    
@login_required(login_url='/login/')
def cancel_booking(request, destination, hotel_name, id ):
    get_booking = Booking.objects.get(user = request.user.id)

    get_booking_history = BookingHistory.objects.get(user=request.user.id,
    room=get_booking.room, booking_date = get_booking.booking_date,
    check_in_date_time = get_booking.check_in_date_time, 
    check_out_date_time = get_booking.check_out_date_time,
    number_of_adult_guest = get_booking.number_of_adult_guest,
    number_of_child_guest = get_booking.number_of_child_guest)

    get_booking_history.isCanceled = True
    get_booking_history.save()

    hr = HotelRoom.objects.get(id = get_booking.room.id)
    hr.isBooked = False
    hr.save()

    get_booking.delete()

    return redirect(f'/{destination}/{hotel_name}/{id}')

@login_required(login_url='/login/')
def booking_history(request):
    bh = BookingHistory.objects.filter(user = request.user.id).order_by('-booking_date')
    context = {'bh':bh}
    return render(request, 'app/booking_history.html' ,context)


    
def error_404(request, exception):
    return HttpResponse('<h1> Page not found </h1>')