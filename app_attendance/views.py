from django.shortcuts import render
import qrcode
from django.http import HttpResponse
from io import BytesIO

# Create your views here.
def Home(request):
    return render(request,'home.html',{})

