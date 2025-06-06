from django.db import models
from django.contrib.auth.models import AbstractUser,User


# Create your models here.
class CustomUser(AbstractUser):
    dob = models.DateField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    phone = models.CharField(null=True,blank=True,max_length=10)

class AutoGenQr(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    qr_code = models.ImageField(upload_to="auto_gen_qrcode/",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LoginRegister(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    person_image = models.ImageField(upload_to='person_image/',blank=True,null=True)

# ---------------------------------------------------------------------
class QRCODE(models.Model):
    data = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.data}  {self.mobile}"
    
class QRCode2(models.Model):  # Changed from QRCode to QRCode2
    name = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qrcodes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


