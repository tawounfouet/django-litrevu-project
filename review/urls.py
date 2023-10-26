## APP (review) urls.py

from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('', views.home, name='home'),
    # user_profile
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('follow_user/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('create-ticket', views.new_ticket, name='new_ticket'),
    path('ticket/<int:pk>', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets', views.TicketListView.as_view(), name='ticket_list'),
    path('create-review', views.new_review, name='new_review'),

    # path('profile/<str:username>/', views.user_profile, name='user_profile'),
    # path('subscriptions/', views.SubscribeView.as_view(), name='subscriptions'),
    # # vue f_sub
    # path('f_sub/', views.f_sub, name='f_sub'),

]
