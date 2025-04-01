from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from app.create_csv import *
# from app.insert_db import *
from django.contrib import admin
from app.api import *
import ai_model
urlpatterns = [

    path('',home),
    path('home/',home),
    path('signup/',filter_page),
    path('login/',filter_page),
    path('logout/',user_logout),
    path('profile/',user_profile),

    path('password-reset',auth_views.PasswordResetView.as_view(template_name ='app/password_reset.html'),
    name = 'password_reset'),

    path('password-reset-done',auth_views.PasswordResetDoneView.as_view(
    template_name = 'app/password_reset_done.html'), 
    name = 'password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
    template_name = 'app/password_reset_confirm.html'),
    name = 'password_reset_confirm'),
     
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
    template_name = 'app/password_reset_complete.html'), name = 'password_reset_complete'),

    path('destination/<str:destination>/hotels', view_hotels),
    path('destination/<str:destination>/hotels/page/<int:pageNo>', view_hotels_by_page),
    path('<str:destination>/<str:hotel_name>/<int:id>', book_hotel),
    path('admin/', admin.site.urls),
    path('cancel/booking/<str:destination>/<str:hotel_name>/<int:id>', cancel_booking),
    path('user/booking_history', booking_history),
    path('api/user_booking_details/<str:un>',api_user_booking_details),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


remove_booking_data()
check_booking_expired()
create_file()
#insert_amenities()
