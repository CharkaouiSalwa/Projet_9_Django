from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Rediriger vers la page suivante
            return redirect('vers la page suivante aprés l''authentification')
        else:
            # Gérer l'erreur d'authentification
            error_message = "Identifiant ou mot de passe incorrect"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            error_message = "Les mots de passe ne correspondent pas."
            return render(request, 'register.html', {'error_message': error_message})
        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=username, password=password)
        # Enregistrer l'utilisateur dans la base de données
        user.save()
        # Rediriger vers une page de succès ou faire d'autres actions
        return redirect('login')
    else:
        return render(request, 'register.html')
