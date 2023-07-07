from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from authentification.views import login_view, register_view, logout_view
from litreview.views import search,\
    unsubscribe, subscriptions,  create_ticket, update_ticket, \
    post, delete_ticket, create_ticket_review, flux, critique_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('search/', search, name='search'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('create_ticket/', create_ticket, name='create_ticket'),
    path('update_ticket/<int:ticket_id>/', update_ticket, name='update_ticket'),
    path('logout/', logout_view, name='logout'),
    path('post/', post, name='post'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('create_ticket_review/', create_ticket_review, name='create_ticket_review'),
    path('flux/', flux, name='flux'),
    path('critique/<int:ticket_id>/', critique_view, name='critique'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




