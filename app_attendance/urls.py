from django.urls import path
from . import views

urlpatterns = [
    path('generate_custom_qrcode/<str:data>/', views.generate_custom_qrcode, name='generate_custom_qrcode'),
]
