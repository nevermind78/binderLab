# Dockerfile
FROM jupyter/base-notebook:latest

# Installer les dépendances avec conda

# Copier le fichier requirements.txt
COPY binder/requirements.txt .

# Installer les dépendances avec pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier les notebooks
COPY labs /home/jovyan/labs
COPY notebooks /home/jovyan/notebooks
# Définir le répertoire de travail
WORKDIR /home/jovyan/

# Commande par défaut
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]