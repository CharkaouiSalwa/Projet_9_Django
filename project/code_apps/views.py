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
            # Rediriger vers une page de succès ou faire d'autres actions
            return redirect('home')
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
        email = request.POST.get('email')
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            error_message = "Ce nom d'utilisateur est déjà pris"
            return render(request, 'register.html', {'error_message': error_message})
        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=username, password=password, email=email)
        # Rediriger vers une page de succès ou une autre vue
        return redirect('home')
    else:
        return render(request, 'register.html')


