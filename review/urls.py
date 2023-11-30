## APP (review) urls.py

from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('feeds/', views.feed, name='feed'),
    # user_profile
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('subscriptions/', views.follow_user, name='subscriptions'),
    path('unfollow/', views.unfollow_user, name='unfollow_user'),
    path('create-ticket', views.TicketCreateView.as_view(), name='new_ticket'),
    path('ticket/<int:pk>', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/<int:pk>/update', views.TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/<int:ticket_id>/delete', views.delete_ticket, name='ticket_delete'),
    path('tickets/', views.TicketReviewListView.as_view(), name='ticket_list'),
    # Review
    path('create-review-blank', views.new_review_blank, name='new_review_blank'),
    path('create-review/<int:ticket_id>', views.new_review, name='new_review'),
    path('reviews', views.ReviewListView.as_view(), name='review_list'),   

]
