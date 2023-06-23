from django.contrib import admin
from django.urls import path
from code_apps.views import login_view, register_view, search,\
    unsubscribe, subscriptions, create_ticket, logout_view, update_ticket


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('search/', search, name='search'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
    path('search/', search, name='subscriptions'),
    path('create_ticket/', create_ticket, name='create_ticket'),
    path('logout/', logout_view, name='logout'),
    path('update_ticket/<int:ticket_id>/', update_ticket, name='update_ticket'),


]




