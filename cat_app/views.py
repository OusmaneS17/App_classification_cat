from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CatDogImageForm
from .utils import predict_Cat_Dog
import os
from django.shortcuts import render

# Create your views here.
# malaria_app/views.py

from django.shortcuts import render, redirect
from .forms import CatDogImageForm
from .utils import predict_Cat_Dog
import os


def index(request):
    return render(request, 'cat_app/home.html')
def home(request):
    if request.method == 'POST':
        form = CatDogImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            
            # Chemin absolu pour le traitement
            image_path = instance.image.path
            prediction_result = predict_Cat_Dog(image_path)
            
            # URL relative pour l'affichage
            image_url = instance.image.url
            
            context = {
                'prediction': prediction_result['class'],
                'confidence': prediction_result['confidence'],
                'prob_cat': prediction_result['prob_cat'],
                'prob_dog': prediction_result['prob_dog'],
                'image_url': image_url,
                'is_dog': prediction_result['class'] == 'Chien'
            }
            return render(request, 'cat_app/result.html', context)
    else:
        form = CatDogImageForm()
    return render(request, 'cat_app/index.html', {'form': form})

@csrf_exempt
def predict_api(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Sauvegarde temporaire du fichier
        temp_path = os.path.join('temp', image_file.name)
        with open(temp_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        
        # Prédiction
        prediction_result = predict_Cat_Dog(temp_path)
        
        # Nettoyage du fichier temporaire
        os.remove(temp_path)
        
        return JsonResponse({
            'status': 'success',
            'prediction': prediction_result['class'],
            'confidence': float(prediction_result['confidence']),
            'prob_cat': float(prediction_result['prob_cat']),
            'prob_dog': float(prediction_result['prob_dog'])
        })
    
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'})