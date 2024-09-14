from django.urls import path
from . import views


from .views import *
from .views import send_friend_request, accept_friend_request, reject_friend_request, view_friend_requests, friends_list
from .views import inbox_view, send_message_view,chat_view,partner_search_view



app_name = 'user'
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('matrimonyhome/',views.matrimonyhome,name='matrimonyhome'),
    path('personaldetails/', PersonalDetailsView.as_view(), name='personaldetails'),
    path('partnerpreferance/',PartnerpreferanceView.as_view(),name='partner_preference'),
    path('grid/', Grid.as_view(), name='grid'),
    path('partner/<int:pk>/', PartnerProfileView.as_view(), name='partner_profile'),  # Add this line

    path('send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject_request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friend_requests/', view_friend_requests, name='friend_requests'),
    path('friends/', friends_list, name='friends_list'),
    path('remove_friend/<int:friend_id>/', remove_friend, name='remove_friend'),



    # Add other URL patterns here
    path('inbox/', inbox_view, name='inbox'),
    path('send_message/<int:user_id>/', send_message_view, name='send_message'),
    path('chatbox/<int:user_id>/', chat_view, name='chatbox'),


    path('add_to_favorites/<int:profile_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:profile_id>/', views.remove_from_favorites, name='remove_from_favorites'),

    path('favorites/', favorites_view, name='favorites'),


    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('failed/', FailedView.as_view(), name='failed'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),


    path('search/', partner_search_view, name='partner_search'),
    
    path('profile-details/', profile_details_view, name='profile_details'),



]