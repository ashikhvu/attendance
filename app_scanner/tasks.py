from celery import shared_task
from .models import *
import qrcode
import datetime
from io import BytesIO
from django.core.files.base import ContentFile
import random

@shared_task(bind=True)
def fun(self):
    # operations
    print("---------You are in Fun function------------")
    return "done"

@shared_task(bind=True)
def generate_qr_code_automatic(self):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    print(random.randint(0,9999999999999999999))
    data = f"QR code generated on {random.randint(0,9999999999999999999)}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    all = AutoGenQr.objects.all()
    all.delete()
    name = f"AutoGenQr_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    qr_instance = AutoGenQr(name=name)
    qr_instance.qr_code.save(name, ContentFile(buffer.read()))
    qr_instance.save()
    return qr_instance.qr_code.url
