import streamlit as st
from PIL import Image
import requests
import subprocess
import time

# Titre de l'application
st.title("Classification d'images avec Fashion MNIST")

# Classes Fashion MNIST
fmnist_classes = [
    "T-shirt/top",  # Classe 0
    "Trouser",      # Classe 1
    "Pullover",     # Classe 2
    "Dress",        # Classe 3
    "Coat",         # Classe 4
    "Sandal",       # Classe 5
    "Shirt",        # Classe 6
    "Sneaker",      # Classe 7
    "Bag",          # Classe 8
    "Ankle boot"    # Classe 9
]

# Fonction pour lancer l'entraînement des modèles
def train_models(train_size):
    # Simuler l'entraînement des modèles (remplacez par votre code d'entraînement réel)
    st.write(f"Entraînement des modèles avec {train_size * 100}% des données...")
    time.sleep(5)  # Simuler un temps d'entraînement
    st.success("Entraînement terminé !")

# Fonction pour lancer l'API Flask
def start_flask_api():
    # Lancer l'API Flask en arrière-plan
    process = subprocess.Popen(["python", "api.py"])  # Remplacez "api_flask.py" par le nom de votre fichier API
    st.write("API Flask démarrée.")
    return process

# Sélection de la proportion train/test
st.header("Configuration de l'entraînement")
train_size = st.slider("Proportion des données pour l'entraînement (train size)", 0.1, 0.9, 0.8, 0.1)

# Bouton pour lancer l'entraînement
if st.button("Lancer l'entraînement"):
    train_models(train_size)
    # Démarrer l'API Flask après l'entraînement
    flask_process = start_flask_api()
    st.session_state.flask_process = flask_process  # Sauvegarder le processus dans la session

# Partie upload et prédiction
st.header("Prédiction")

# URL de l'API Flask (remplacez par l'URL de votre API si nécessaire)
API_URL = "http://127.0.0.1:5000/predict"

# Téléchargement de l'image
uploaded_file = st.file_uploader("Téléchargez une image (28x28 pixels)", type=["png", "jpg", "jpeg"])

# Afficher l'image téléchargée une seule fois
if uploaded_file is not None:
    # Réinitialiser le pointeur du fichier pour éviter l'erreur PIL
    uploaded_file.seek(0)
    
    # Ouvrir l'image
    image = Image.open(uploaded_file).convert('L')  # Convertir en niveaux de gris
    
    # Centrer l'image
    col1, col2, col3 = st.columns([1, 2, 1])  # Crée 3 colonnes, la colonne du milieu est plus large
    with col2:  # Utilise la colonne du milieu pour centrer l'image
        st.image(image, caption="Image téléchargée", width=150)  # Ajustez la largeur selon vos besoins

# Sélection du modèle
model_name = st.selectbox(
    "Sélectionnez un modèle",
    ["Logistic Regression", "Linear SVC", "KNN"]
)

# Bouton pour lancer la prédiction
if st.button("Prédire"):
    if uploaded_file is not None:
        # Réinitialiser le pointeur du fichier
        uploaded_file.seek(0)
        
        # Envoyer la requête à l'API Flask
        files = {"file": uploaded_file}
        data = {"model": model_name}
        response = requests.post(API_URL, files=files, data=data)

        # Afficher le résultat
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")  # Correction : "prediction" -> "prediction"
            
            # Afficher la prédiction
            class_name = fmnist_classes[prediction]  # Convertir le numéro en nom de classe
            st.success(f"**Prédiction :** {class_name} (Classe {prediction})")
        else:
            st.error(f"Erreur lors de la prédiction : {response.text}")
    else:
        st.warning("Veuillez télécharger une image avant de lancer la prédiction.")