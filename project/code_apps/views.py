from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Ticket, UserFollows, Review
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm
from django.urls import reverse


from django.contrib import messages



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
        try:
            # Vérifier si l'utilisateur existe déjà
            User.objects.get(username=username)
            error_message = "Nom d'utilisateur déjà utilisé."
            return render(request, 'register.html', {'error_message': error_message})
        except User.DoesNotExist:
            # Créer un nouvel utilisateur
            user = User.objects.create_user(username=username, password=password)
            # Enregistrer l'utilisateur dans la base de données
            user.save()
            # Rediriger vers une page de succès ou faire d'autres actions
            messages.success(request, "Inscription réussie. Vous pouvez vous connecter maintenant.")
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

    return redirect('search')

@login_required
def followers(request):
    user = request.user
    followers = UserFollows.objects.filter(followed_user=user)
    context = {
        'followers': followers
    }
    return render(request, 'search.html', context)


@login_required
def post(request):
    # Récupérer les tickets de l'utilisateur connecté
    tickets = Ticket.objects.filter(user=request.user)
    # Récupérer les critiques associées aux tickets de l'utilisateur
    reviews = Review.objects.filter(ticket__in=tickets)
    return render(request, 'post.html', {'tickets': tickets, 'reviews': reviews})
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('post')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('post')  # Redirection vers la page de connexion
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'update_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    # Récupérer le ticket à supprimer
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('post')
    return render(request, 'delete_ticket.html', {'ticket': ticket})


from django.shortcuts import render, redirect
from .forms import TicketForm, ReviewForm

def create_ticket_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')  # Rediriger vers la page Flux après la création
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'create_ticket_review.html', {'ticket_form': ticket_form, 'review_form': review_form})


def flux(request):
    following_users = request.user.following.all().values('followed_user')
    followed_user_ids = [user['followed_user'] for user in following_users]
    followed_users = User.objects.filter(id__in=followed_user_ids)
    tickets = Ticket.objects.filter(user__in=followed_users)

    for ticket in tickets:
        critiques = Review.objects.filter(ticket=ticket)
        ticket.critiques = critiques

    return render(request, 'flux.html', {'tickets': tickets})



def critique_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Sauvegarde de la critique
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')

    else:
        form = ReviewForm()
    return render(request, 'critique.html', {'form': form, 'ticket': ticket})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion


