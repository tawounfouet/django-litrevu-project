## APP (review) urls.py

from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('create-ticket', views.new_ticket, name='new_ticket'),
    path('ticket/<int:pk>', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets', views.TicketListView.as_view(), name='ticket_list'),
    path('create-review', views.new_review, name='new_review'),

]
