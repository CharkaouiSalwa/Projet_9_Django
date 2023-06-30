from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from code_apps.views import login_view, register_view, search,\
    unsubscribe, create_ticket, update_ticket,logout_view,user_tickets , delete_ticket,create_ticket_review


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('search/', search, name='search'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),


    path('create_ticket/', create_ticket, name='create_ticket'),
    path('update_ticket/<int:ticket_id>/', update_ticket, name='update_ticket'),
    path('logout/', logout_view, name='logout'),
    path('user_tickets/', user_tickets, name='user_tickets'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('create_ticket_review/', create_ticket_review, name='create_ticket_review'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




