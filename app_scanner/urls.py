# qrcode_scanner/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('scan_qr/', views.scan_qr, name='scan_qr'),
    path('scan_qr2/', views.scan_qr2, name='scan_qr2'),
    path('testView', views.testView,name="testView"),
    path('autogenerate_qr', views.autogenerate_qr,name="autogenerate_qr"),
    path('fetch_qr', views.fetch_qr,name="fetch_qr"),
    path('register_user', views.register_user,name="register_user"),
]
