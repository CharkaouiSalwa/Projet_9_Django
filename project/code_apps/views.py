from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .models import Ticket, UserFollows, Review
from django.contrib.auth.decorators import login_required
from .forms import TicketForm



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Rediriger vers la page suivante
            return redirect('search')
        else:
            # Gérer l'erreur d'authentification
            error_message = "Identifiant ou mot de passe incorrect"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

@login_required
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

@login_required
def search(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user is not None:
            UserFollows.objects.get_or_create(user=request.user, followed_user=user)
        try:
            user = User.objects.get(username=username)
            UserFollows.objects.get_or_create(user=request.user, followed_user=user)
        except User.DoesNotExist:
            pass
    subscriptions = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'search.html', {'subscriptions': subscriptions, 'followers': followers})


@login_required
def subscriptions(request):
    # Récupérer la liste des abonnements de l'utilisateur connecté cest méthode Read de CRUD lors de chargement de la page
    user = request.user
    subscriptions = UserFollows.objects.filter(user=user)
    return render(request, 'subscriptions.html', {'subscriptions': subscriptions})


@login_required
def unsubscribe(request, user_id):
    # Recherche de l'objet UserFollows correspondant à l'utilisateur et à l'utilisateur suivi
    try:
        subscription = UserFollows.objects.get(user=request.user, followed_user_id=user_id)
        # Suppression de l'objet UserFollows : delete dans CRUD
        subscription.delete()
    except UserFollows.DoesNotExist:
        pass

    return redirect('subscriptions')

@login_required
def followers(request):
    user = request.user
    followers = UserFollows.objects.filter(followed_user=user)
    context = {
        'followers': followers
    }
    return render(request, 'search.html', context)



def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('login')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})


def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirection vers la page de connexion
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'update_ticket.html', {'form': form, 'ticket': ticket})






def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion


