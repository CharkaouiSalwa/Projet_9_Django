from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Rediriger vers la page suivante
            return redirect('flux')
        else:
            # Gérer l'erreur d'authentification
            error_message = "Identifiant ou mot de passe incorrect"
            return render(request, 'authentification/login.html', {'error_message': error_message})
    else:
        return render(request, 'authentification/login.html')

def register_view(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            error_message = "Les mots de passe ne correspondent pas."
            return render(request, 'authentification/register.html', {'error_message': error_message})
        try:
            # Vérifier si l'utilisateur existe déjà
            User.objects.get(username=username)
            error_message = "Nom d'utilisateur déjà utilisé."
            return render(request, 'authentification/register.html', {'error_message': error_message})
        except User.DoesNotExist:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(username=username, password=password)
            # Enregistrer l'utilisateur dans la base de données
            user.save()
            # Rediriger vers une page de succès ou faire d'autres actions
            messages.success(request, "Inscription réussie. Vous pouvez vous connecter maintenant.")
            return redirect('login')
    else:
        return render(request, 'authentification/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion
