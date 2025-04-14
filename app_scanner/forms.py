# forms.py
from django.contrib.auth import get_user_model
from django import forms

class QRCodeUploadForm(forms.Form):
    qr_code = forms.ImageField()

user = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ["first_name","last_name","username","password","email","dob","address"]
