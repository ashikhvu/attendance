# qrcode_scanner/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('generate_qr/', views.generate_qr, name='generate_qr'),
    path('scan_qr/', views.scan_qr, name='scan_qr'),
    path('scan_qr2/', views.scan_qr2, name='scan_qr2'),
    path('testView', views.testView,name="testView"),
    path('autogenerate_qr', views.autogenerate_qr,name="autogenerate_qr"),
    path('fetch_qr', views.fetch_qr,name="fetch_qr"),
    path('register_user', views.register_user,name="register_user"),
    path('login',auth_views.LoginView.as_view(template_name='qr_login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='qr_logout.html'),name='logout'),
    path('check_qr_valid', views.check_qr_valid,name="check_qr_valid"),
    path('log_register', views.log_register,name="log_register"),
    path('login_success', views.login_success,name="login_success"),
]
