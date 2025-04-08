from django.shortcuts import render
import qrcode
from django.http import HttpResponse
from io import BytesIO

# Create your views here.
def generate_custom_qrcode(request, data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return HttpResponse(img_io, content_type='image/png')
