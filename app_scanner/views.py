# views.py
from django.shortcuts import render,redirect
import qrcode
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from pathlib import Path
from .models import *
from PIL import Image
from pyzbar.pyzbar import decode
from celery import shared_task
import datetime
from django.http import HttpResponse
from .tasks import generate_qr_code_automatic
from django.http import JsonResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def autogenerate_qr(request):
    img = AutoGenQr.objects.all().last()
    return render(request,'autogenerate_qr.html',{'qr_code_instance':img})

def fetch_qr(request):
    qr = AutoGenQr.objects.all().last()
    if qr:
        img_url = qr.qr_code.url
    return JsonResponse({"img":img_url})

def register_user(request):
    form=None
    form = CustomUserForm()
    print('enter')
    if request.method=="POST":
        print('post')
        form = CustomUserForm(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect('login')
        else:
            print(f'not valid {form.errors}')

    return render(request,"register.html",{'form':form})

def generate_qr(request):
    qr_image_url = None
    if request.method=="POST":
        mobile   = request.POST.get('mob_no')
        data = request.POST.get('qr_data')
        if not mobile or len(mobile) != 10 or not mobile.isdigit():
            return render(request,'generate_qr.html',{'error':'invalid mobile number'})
        qr_content = f"{data}|{mobile}"
        qr = qrcode.make(qr_content)
        qr_image_io = BytesIO()
        qr.save(qr_image_io,'PNG')
        qr_image_io.seek(0)
        qr_storage_path = settings.MEDIA_ROOT / 'qr_codes'
        fs = FileSystemStorage(location=qr_storage_path,base_url='/media/qr_codes/')
        file_name = f"{data}_{mobile}.png"
        qr_image_content = ContentFile(qr_image_io.read(),name=file_name)
        file_path = fs.save(file_name,qr_image_content)
        qr_image_url = fs.url(file_name)
        QRCODE.objects.create(
            data=data,
            mobile=mobile
        )
    return render(request,'generate_qr.html',{'qr_image_url':qr_image_url})

def scan_qr(request):
    result = None
    if request.method=="POST" and request.FILES.get('qr_image'):
        mobile   = request.POST.get('mob_no')
        qr_image = request.FILES['qr_image']
        if not mobile or len(mobile) != 10 or not mobile.isdigit():
            return render(request,'scan_qr.html',{'error':'invalid mobile number'})
        fs = FileSystemStorage()
        filename = fs.save(qr_image.name,qr_image)
        image_path = Path(fs.location) / filename
        try:
            image= Image.open(image_path)
            decoded_objects = decode(image)
            if decoded_objects: 
                qr_content = decoded_objects[0].data.decode('utf-8').strip()
                qr_data , qr_mob_no = qr_content.split('|')
                qr_entry=QRCODE.objects.filter(data = qr_data,mobile=qr_mob_no).last()
                if qr_entry and mobile==qr_mob_no :
                    result = "Scan Success : valid qrcode for the provided mobile number"
                    qr_entry.delete()
                    qr_image_path = settings.MEDIA_ROOT / "qr_codes" / f"{qr_data}_{qr_mob_no}.png"
                    if qr_image_path.exists():
                        qr_image_path.unlink()
                    if image_path.exists():
                        image_path.unlink()
                else:
                    result = "Error : Invalid QRcode or mobile number mismatch"
            else:
                result = "Error : No QR Code detected in the image"
        except Exception as e:
            result = f"Error processing the image : {str(e)}"
        finally:
            if image_path.exists():
                image_path.unlink()
    return render(request,'scan_qr.html',{'result':result})

@login_required
def scan_qr2(request):
    return render(request, 'scan_qr2.html')


# yourapp/tasks.py

@shared_task
def generate_qr_code():
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Use current date or custom string for the QR
    data = f"QR code generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to an in-memory file
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Create a Django file from the image and save it to the model
    qr_code_instance = QRCode2.objects.create(  # Changed to QRCode2
        name=f"QRCode2_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    qr_code_instance.qr_code.save(f"qrcodes/{qr_code_instance.name}.png", ContentFile(buffer.read()))
    qr_code_instance.save()

    # Optionally, return the path to the saved file
    return qr_code_instance.qr_code.url

from .tasks import fun

def testView(request):
    fun.delay()
    return HttpResponse("Done")

import hashlib

def file_hash(file):
    """Returns an MD5 hash of the file content"""
    hasher = hashlib.md5()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

@login_required
def check_attendance_marked_or_not(request):
    qr_code = request.POST.get('qr_code')
    print(qr_code)
    obj = AutoGenQr.objects.all().last()
    
    try:
        # Load the QR code image from the file system
        image_path = obj.qr_code.path  # assumes qr_code is an ImageField
        img = Image.open(image_path)

        # Decode the QR code image
        decoded_objs = decode(img)
        if not decoded_objs:
            return JsonResponse({"errors": "Failed to decode QR code image"}, status=400)

        decoded_text = decoded_objs[0].data.decode('utf-8')  # get first QR result
        print(f"Decoded from image: {decoded_text}")

        if decoded_text == qr_code:
            print('matched')
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            already_marked = LoginRegister.objects.filter(
                user=request.user,
                created_at__range=(today_start, today_end)
            ).exists()
            if not already_marked:
                return JsonResponse({"success": "Take a selfie and confirm your attendance!"})
            else:
                return JsonResponse({"success": "Already marked attendance today!"})
        else:
            return JsonResponse({"errors": "QR code does not match"}, status=400)

    except Exception as e:
        # return JsonResponse({"errors": str(e)}, status=500)
        return JsonResponse({"errors": "QR code does not match"}, status=500)
    

@login_required
def confirm_attendance(request):
    # try:
    if request.method=="POST":
        if request.FILES:
            person_image = request.FILES['person_image']
        else:
            person_image = None
        location = request.POST.get('location')
        log_reg = LoginRegister(
            user=request.user,
            person_image = person_image,
            location = location
        )
        log_reg.save()
    return JsonResponse({'success':'Attendance Marked Successfully !'})
    # except Exception as e:
    #     return JsonResponse({"errors":str(e)},status=400)
    
    
@login_required
def log_register(request):
    reg = LoginRegister.objects.filter()
    for i in reg:
        print(f'---------------{i.created_at}-----------')

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    print(f'--------------{now}---------------')
    return render(request,'log_register.html',{'reg':reg})

@login_required
def login_success(request):
    return render(request,"login_success.html",{})