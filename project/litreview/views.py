from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from litreview.models import Ticket, UserFollows, Review
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from litreview.forms import TicketForm, ReviewForm

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
    return render(request, 'litreview/search.html', {'subscriptions': subscriptions, 'followers': followers})

@login_required
def subscriptions(request):
    # Récupérer la liste des abonnements de l'utilisateur connecté cest méthode Read de CRUD lors de chargement de la page
    user = request.user
    subscriptions = UserFollows.objects.filter(user=user)
    return render(request, 'litreview/subscriptions.html', {'subscriptions': subscriptions})


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
    return render(request, 'litreview/search.html', context)


@login_required
def post(request):
    # Récupérer les tickets de l'utilisateur connecté
    tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')
    # Récupérer les critiques associées aux tickets de l'utilisateur
    reviews = Review.objects.filter(ticket__in=tickets)
    return render(request, 'litreview/post.html', {'tickets': tickets, 'reviews': reviews})

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
    return render(request, 'litreview/create_ticket.html', {'form': form})

@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('post')  # Redirection vers la post
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'litreview/update_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    # Récupérer le ticket à supprimer
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('post')
    return render(request, 'litreview/delete_ticket.html', {'ticket': ticket})

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

    return render(request, 'litreview/create_ticket_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

def flux(request):
    following_users = request.user.following.all().values('followed_user')
    followed_user_ids = [user['followed_user'] for user in following_users]
    followed_users = User.objects.filter(id__in=followed_user_ids)
    tickets = Ticket.objects.filter(user__in=followed_users).order_by('-time_created')

    for ticket in tickets:
        critiques = Review.objects.filter(ticket=ticket)
        ticket.critiques = critiques

    return render(request, 'litreview/flux.html', {'tickets': tickets})



@login_required
def critique_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    try:
        critique = Review.objects.get(ticket=ticket)
        return redirect('update_critique', critique_id=critique.id, ticket_id=ticket_id)
    except Review.DoesNotExist:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                critique = form.save(commit=False)
                critique.ticket = ticket
                critique.user = request.user
                critique.save()
                return redirect('flux')
        else:
            form = ReviewForm()
    return render(request, 'litreview/critique.html', {'form': form, 'ticket': ticket})

@login_required
def update_critique(request, critique_id, ticket_id):
    critique = get_object_or_404(Review, id=critique_id, ticket_id=ticket_id)
    ticket = get_object_or_404(Ticket, id=ticket_id)  # Récupérer le ticket correspondant

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=critique)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = ReviewForm(instance=critique)

    return render(request, 'litreview/update_critique.html', {'form': form, 'critique': critique, 'ticket': ticket})

