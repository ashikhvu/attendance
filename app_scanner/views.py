# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import QRCodeUploadForm
from pyzbar.pyzbar import decode
from PIL import Image
import io

def extract_qr_code_data(request):
    if request.method == 'POST' and request.FILES.get('qr_code'):
        form = QRCodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            image_file = request.FILES['qr_code']
            
            # Open the image file using PIL
            image = Image.open(image_file)
            
            # Decode the QR code from the image
            qr_codes = decode(image)
            
            # If QR code found, extract the data
            if qr_codes:
                qr_data = qr_codes[0].data.decode('utf-8')  # Get the data of the first QR code found
                return HttpResponse(f'QR Code Data: {qr_data}')
            else:
                return HttpResponse('No QR Code found in the image.')
    else:
        form = QRCodeUploadForm()

    return render(request, 'upload_qr_code.html', {'form': form})