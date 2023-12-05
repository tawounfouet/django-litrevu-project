
# Application Web Django de gestion des revues (reviews)

<p align="center">
  <img src="https://user.oc-static.com/upload/2023/06/29/168805567091_LITrevu%20banner.png" alt="Logo & Banner LITRevue"/>
</p>

Developpement d'une application web django permettant à une communauté d'utilisateurs de publier des critiques de livres ou d’articles et de consulter ou de solliciter une critique de livres à la demande.


## Prérequis
Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :
- Python (version 3.x recommandée)
- pip (installé avec Python par défaut)
- Virtualenv (pour isoler l'environnement Python)

## Installation
1. Cloner le projet sur votre machine
```bash
git clone https://github.com/tawounfouet/django-litrevu-project.git

cd django-litrevu-project
```

2. Créer un environnement virtuel et l'activer
```bash
virtualenv env

source env/bin/activate
```

3. Installer les dépendances du projet
```bash
pip install -r requirements.txt
```

4. Lancez le serveur de développement Django :
```bash
python manage.py runserver
```

5. Rendez-vous sur http://localhost:8000/ pour voir le résultat !


6. Identifiants de connexion
```bash
# Superuser
username: awf
password: awf

# Utilisateur test
username: staff1
password: Thomson1995
```

## Auteur
- [Thomas AWOUNFOUET]()
