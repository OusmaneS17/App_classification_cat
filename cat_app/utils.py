# malaria_app/utils.py
import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from django.conf import settings

def load_Cat_Dog_model():
    # Chemin absolu vers le modèle
    model_path = os.path.join(settings.BASE_DIR, 'cat_app', 'models', 'model_mobilenet_cat_dogs.h5')
    return load_model(model_path)

def predict_Cat_Dog(image_path):
    model = load_Cat_Dog_model()
    
    # Prétraitement de l'image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))  # Assurez-vous que cette taille correspond à l'entrée attendue par votre modèle
    img = img_to_array(img)
    img = img / 255.0  # Normalisation
    img = np.expand_dims(img, axis=0)
    
    # Prédiction
    prediction = model.predict(img)
    
    # Interprétation des résultats selon le type de sortie du modèle
    if prediction.shape[1] == 1:  # Modèle avec activation sigmoid (sortie unique)
        prob_dog = float(prediction[0][0])
        prob_cat = 1 - prob_dog
        class_idx = 0 if prob_dog > 0.5 else 1
        confidence = prob_dog if class_idx == 0 else prob_cat
    else:  # Modèle avec activation softmax (2 sorties)
        prob_cat = float(prediction[0][0])
        prob_dog = float(prediction[0][1])
        class_idx = np.argmax(prediction[0])
        confidence = max(prob_cat, prob_dog)
    
    classes = ["Chien","Chat"]
    
    return {
        'class': classes[class_idx],
        'confidence': confidence,
        'prob_cat': prob_cat,
        'prob_dog': prob_dog
    }