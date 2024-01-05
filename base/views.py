# views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import pytesseract
import os
import cv2

def home(request):
    return render(request, 'base/home.html')

def upload_image(request):
    if request.method == 'POST':
        # Récupérer l'image depuis le formulaire
        uploaded_image = request.FILES.get('image')
        uploaded_document = request.FILES.get('document')

        # Enregistrer l'image dans le système de fichiers (à adapter selon vos besoins)
        if uploaded_image:
            fs = FileSystemStorage()
            image_filename = fs.save(uploaded_image.name, uploaded_image)
            image_path = fs.url(image_filename)
            image_full_path = os.path.join("C:\\Users\\Dell\\Desktop\\ocr\\ocr_project", image_path[1:])
            
            # Effectuer l'OCR sur l'image
            ocr_result_image = perform_ocr(image_full_path)
            print(".............................")
        else:
            ocr_result_image = None

        # Enregistrer le document dans le système de fichiers (à adapter selon vos besoins)
        if uploaded_document:
            fs = FileSystemStorage()
            document_filename = fs.save(uploaded_document.name, uploaded_document)
            document_path = fs.url(document_filename)
            
            # Effectuer le traitement sur le document
            process_document(document_path)
        else:
            document_path = None

        # Obtenez le nom de l'image sans extension
        scanned_image_name = os.path.splitext(uploaded_image.name)[0]
        print('????????????????????')
        print(image_full_path)
        print('????????????????????')


        # Passer les données à la template result.html
        return render(request, 'base/result.html', {'image_path': image_full_path, 'ocr_result_image': ocr_result_image, 'document_path': document_path, 'scanned_image_name': scanned_image_name})

    return HttpResponseRedirect(reverse('home'))

def perform_ocr(image_path):
    # Utiliser pytesseract pour effectuer l'OCR (à adapter selon vos besoins)
    # (Remplacez ceci par votre code d'OCR réel)
    image = cv2.imread(image_path)
    Himg , Wimg , _ = image.shape
    c= r"--psm 11 --oem 1"
    boxes = pytesseract.image_to_data(image, lang="fra+ara",config=c)
    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b)==12:
                x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                cv2.rectangle(image,(x,y),(w+x,y+h),(0,255,0),3)
                cv2.putText(image,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
                print(b[11])
    
    ocr_result = pytesseract.image_to_string(image_path)
    print('////////////////////////////////')
    print(ocr_result)
    print('??????????????????????????????')
    return ocr_result

def process_document(document_path):
    # Effectuer le traitement sur le document (à adapter selon vos besoins)
    pass
