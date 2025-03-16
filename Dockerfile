# Dockerfile
FROM jupyter/base-notebook:latest

# Installer les dépendances avec conda
COPY binder/environment.yml .
RUN conda env update -n base -f environment.yml && \
    conda clean -afy && \
    pip install fancyimpute>=0.7.0

# Copier les notebooks
COPY notebooks /home/jovyan/notebooks

# Définir le répertoire de travail
WORKDIR /home/jovyan/notebooks

# Commande par défaut
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]