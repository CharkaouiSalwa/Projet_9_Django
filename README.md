

# Projet 9: Développez une application Web en utilisant Django
***

### ***Contexte :***
L'objectif du projet est de commercialiser un produit permettant à une communauté d'utilisateurs de
consulter ou de solliciter une critique de livres à la demande.
***
### ***Installation :***

 - Télécharger le projet depuis [Github](https://github.com/CharkaouiSalwa/Projet_9_Django.git)
 - Se positionner dans le dossier git téléchargé
 - Créer un environnement virtuel :
```
python -m venv env
```
 - Activer l'environnement virtuel : 
```
source  env/bin/activate
```
 - Installer les bibliothéques nécessaires depuis le fichier requirements.txt :
``` shell
pip install -r requirements.txt
```
***
### ***Initialisation de la base de données :***
- Accédez au dossier de travail.
```
cd project
```
- Procédez à une recherche de migrations.
```
python manage.py makemigrations
```
- Lancer les migrations nécessaires.
```
python manage.py migrate
```
### ***Utilisation :***
- Démarrage du serveur local Accédez et au dossier de travail.
```
cd project
```
- Démarrez le serveur local.
```
python manage.py runserver
```
- Navigation :
Accédez au site sur votre navigateur depuis l'url(http://127.0.0.1:8000/)
### ***Exécution :*** 
Pour vous connecter à l'application vous avez besoin de créer un compte ou bien d'utiliser un compte déjà enregistrer.

Compte disponible pour l'exemple : 
```
Identifiant : malak

Mot de passe : malak
```
```
Identifiant : openclassrooms

Mot de passe : openclassrooms
```
Sinon en cliquant sur S'inscrire vous pourrez créer un compte afin de vous identifier. Lorsque vous serez connecté, vous serez redirigé vers votre page d'accueil.

<br/><br/><br/>
*Par Salwa CHARKAOUI* 




