# qrcode_scanner/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload_qr_code/', views.extract_qr_code_data, name='upload_qr_code'),
]
