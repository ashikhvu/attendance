# forms.py
from django import forms

class QRCodeUploadForm(forms.Form):
    qr_code = forms.ImageField()
