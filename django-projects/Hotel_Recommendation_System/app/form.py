from django import forms
from django.forms import TextInput, PasswordInput
from django.contrib.auth.models import User
from datetime import datetime
from app.models import Booking


IMG_EXTENSION = ['jpeg', 'jpg', 'png']

def is_valid_file(fileName):
    fn = fileName.split('.')
    if fn[1].lower() in IMG_EXTENSION:
        return True
    else:
        return False

def is_valid_dob(year):
    date = datetime.now()
    age = date.year - year
    if age >= 18:
        return True
    else:
        return False 



class SignUpForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    dob = forms.DateField(label='D.O.B', widget= forms.TextInput(attrs={'type':'date'}))
    user_img = forms.FileField(label='Upload your image', required=False)

    def clean_password(self, *args, **kwargs):
        pwd = self.cleaned_data.get('password')
        cpwd = self.cleaned_data.get('confirm_password')

        if len(pwd) >= 8:
            return pwd
        else:
            raise forms.ValidationError('Minimum length of password should be 8') 
      

    def clean_confirm_password(self, *args, **kwargs):
        pwd = self.cleaned_data.get('password')
        cpwd = self.cleaned_data.get('confirm_password')

        if pwd != cpwd:
            raise forms.ValidationError('Confirm password should be same as entered password')
        else:
            return cpwd

    def clean_username(self, *args, **kwargs):
        un = self.cleaned_data.get('username')
        getUsername = User.objects.filter(username = un).exists()
        if getUsername:
            raise forms.ValidationError('This username already exists')
        else:
            return un

    def clean_dob(self, *args, **kwargs):
        d_o_b = str(self.cleaned_data.get('dob'))
        sp_dob = d_o_b.split('-')
        year = int(sp_dob[0])

        if is_valid_dob(year):
            return d_o_b
        else:
            raise forms.ValidationError('Your age should be greater or equal to 18.')
    
    def clean_user_img(self, *args, **kwargs):
        img = self.cleaned_data.get('user_img')
        
        if img is None:
            return img

        if  img is not None:
            fileName = img.name
            if is_valid_file(fileName):
                return img
            else:
                raise forms.ValidationError('(JPEG, JPG and PNG) extension file only allowed.')

    def clean_email(self,*args,**kwargs):
        em = self.cleaned_data.get('email')
        is_email_exists = User.objects.filter(email = em).exists()

        if is_email_exists:
            raise forms.ValidationError('This email already exists.')
        else:
            return em


#class HotelBookingForm(forms.Form):
    



# class LoginForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password']
#         labels = {'username':'Username','password':'Password'}
#         widgets = {'password':forms.PasswordInput}