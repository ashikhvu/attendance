from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model

user = get_user_model()
# Register your models here.
admin.site.register(AutoGenQr)
admin.site.register(user)
admin.site.register(LoginRegister)