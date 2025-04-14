# forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class QRCodeUploadForm(forms.Form):
    qr_code = forms.ImageField()

user = get_user_model()

class CustomUserForm(UserCreationForm):

    email = forms.EmailField()
    password = forms.PasswordInput()
    dob = forms.DateField(widget=forms.DateInput(
        attrs={
            'type':'date'
        }
    ))
    phone= forms.CharField(widget=forms.NumberInput(
        attrs={
            'type':'number',
            'max':999999999
        }
    ))

    class Meta:
        model = user
        fields = ["first_name","last_name","username","password1","password2","email","dob","address","phone"]
