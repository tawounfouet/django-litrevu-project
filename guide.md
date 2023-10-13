

## Initialisation du projet
```bash
# création de l'environnement virtuel avec virtualenv
virtualenv -p python3 .envlitrevu

# activation de l'environnement virtuel
source .envlitrevu/bin/activate

# installlation de django
pip install django

# création du projet django litrevu
django-admin startproject litrevu

# cd dans le projet
cd litrevu



# création de l'application de gestion des revues
python manage.py startapp reviews


# Lance le serveur de développement
python manage.py runserver 8099
```

## Initialisation du depot git
```bash
# Initialisation du dépot git
git init

# Ajout des fichiers à suivre
git add .

# Premier commit
git commit -m "Initial commit"

# Création du dépot sur github
# Ajout du remote
git remote add origin

# Push du code sur github
git push -u origin master
```

## Configuration du projet
```bash
# Création du fichier .gitignore
touch .gitignore

# Ajout des fichiers à ignorer
echo "db.sqlite3" >> .gitignore
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "media/" >> .gitignore
echo "static/" >> .gitignore

# Création du fichier requirements.txt
pip freeze > requirements.txt

pip install -r requirements.txt

# Création du fichier README.md
touch README.md
```

## Initialisation de la base de données
```bash
# Création des migrations
python manage.py makemigrations

# Application des migrations
python manage.py migrate
```

## création de l'application d'authentification
```bash
# création de l'application d'authentification
python manage.py startapp authentication 
python manage.py startapp core  


# Ajout de l'application d'authentification dans le settings.py
INSTALLED_APPS = [
    ...
    ...
    'authentication',
    ...
    ...
]

# création d'un modèle uttilisateur personnalisé
# dans le fichier authentication/models.py
class User(AbstractUser):
    pass

# install de pillow pour le traitement des images
pip install pillow

# dans le fichier settings.py
AUTH_USER_MODEL = 'authentication.User'

# Création des migrations
python manage.py makemigrations

# Application des migrations
python manage.py migrate

# Création d'un super utilisateur
python manage.py createsuperuser

python manage.py runserver 8081
```

```bash

```