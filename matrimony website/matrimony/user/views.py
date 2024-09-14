from django.shortcuts import render,redirect,get_object_or_404
from.forms import PersonalDetailForm,PartnerPreferanceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from.models import PersonalDetails,PartnerPreferance,Subscription
from django.urls import reverse_lazy,reverse
from django.views.generic import View, TemplateView, DetailView, UpdateView, FormView
from account.models import User
from django.db.models import Q
from datetime import date
from .models import FriendRequest,Friend
from django.contrib.auth import get_user_model
from .models import Message, User,Favorite
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from .models import Subscription, User
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from account.models import User  

from urllib.parse import urlencode













User = get_user_model()

# Create your views here.
@login_required
def home(request):
    print("Home view called")
    personal_details = PersonalDetails.objects.filter(user=request.user).first()
    if personal_details:
        print("PersonalDetails found:", personal_details)
        is_personal_details_filled = personal_details.is_filled()
        print(f"Personal details filled: {is_personal_details_filled}")
    else:
        print("No PersonalDetails found for the user.")
        is_personal_details_filled = False
    return render(request, 'home.html', {'is_personal_details_filled': is_personal_details_filled})


def about(request):
    return render(request,'about.html')

def matrimonyhome(request):
    return render(request,'matrimonyhome.html')


class PersonalDetailsView(LoginRequiredMixin, UpdateView):
    model = PersonalDetails
    form_class = PersonalDetailForm
    template_name = 'personaldet.html'
    success_url = reverse_lazy('user:partner_preference')  # Ensure this URL exists in your URLconf

    def get_success_url(self):
        # Check if the partner preference form is filled
        partner_preference = PartnerPreferance.objects.filter(user=self.request.user).first()
        if partner_preference and partner_preference.is_filled() and self.object.is_filled():
            return reverse_lazy('user:partner_preference')
        return reverse_lazy('user:partner_preference')

    

    def get_object(self, queryset=None):
        # Ensure we get the PersonalDetails object for the logged-in user, creating one if it doesn't exist
        obj, created = PersonalDetails.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        print("Form data:", form.cleaned_data)  # Print the cleaned data
        response = super().form_valid(form)
        print("Form is valid, redirecting to:", self.get_success_url())
        return response
    
    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

    

class PartnerpreferanceView(LoginRequiredMixin, UpdateView):
    model = PartnerPreferance
    form_class = PartnerPreferanceForm
    template_name = 'partner.html'
    success_url = reverse_lazy('user:grid')  # Replace 'success_url' with your actual success URL name

    def get_success_url(self):
        # Check if the personal details form is filled
        personal_details = PersonalDetails.objects.filter(user=self.request.user).first()
        if personal_details and personal_details.is_filled() and self.object.is_filled():
            return reverse_lazy('user:grid')
        return reverse_lazy('user:grid')

    def get_object(self, queryset=None):
        obj, created = PartnerPreferance.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        # Ensure the user is set correctly
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)
    


class Grid(LoginRequiredMixin, TemplateView):
    template_name = 'partners_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            partner_preference = user.partner_preference  # Use the correct related name
            profiles = User.objects.filter(
                age__gte=partner_preference.age_min,
                age__lte=partner_preference.age_max,
                personaldetails__caste=partner_preference.caste,
                personaldetails__religion=partner_preference.religion,
                personaldetails__height__gte=partner_preference.height_min,
                personaldetails__height__lte=partner_preference.height_max,
                personaldetails__weight__gte=partner_preference.weight_min,
                personaldetails__weight__lte=partner_preference.weight_max,
                personaldetails__income__gte=partner_preference.income_min,
                personaldetails__income__lte=partner_preference.income_max,
                gender=partner_preference.gender,
                 qualification=partner_preference.qualification
            ).exclude(id=user.id).select_related('personaldetails').prefetch_related('personaldetails')
            context['profiles'] = profiles
        except PartnerPreferance.DoesNotExist:
            context['profiles'] = User.objects.none()  # If no partner preference, show no profiles
            for profile in profiles:
                print(f"Profile ID: {profile.pk}, Username: {profile.username}")

        except PartnerPreferance.DoesNotExist:
            context['profiles'] = User.objects.none() 

        return context


class PartnerProfileView(DetailView):
    model = User
    template_name = 'partner_profile.html'
    context_object_name = 'partner'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner = self.object  # This is the User object for the partner

        # Check if the current user has an active subscription
        user_subscription = Subscription.objects.filter(user=self.request.user, active=True).exists()

        # Get partner preferences if available
        try:
            preference = PartnerPreferance.objects.get(user=partner)
        except PartnerPreferance.DoesNotExist:
            preference = None

        # Add subscription status and preference to the context
        context['has_subscription'] = user_subscription
        context['preference'] = preference
        
        return context
    


# @login_required
# def send_friend_request(request, user_id):
#     to_user = get_object_or_404(User, id=user_id)
    
#     # Check if they are already friends
#     if Friend.objects.filter(
#         (Q(current_user=request.user) & Q(users=to_user)) | 
#         (Q(current_user=to_user) & Q(users=request.user))
#     ).exists():
#         messages.info(request, "You are already friends with this user.")
#         return redirect(request.GET.get('next', 'user:grid'))
    
#     # Check if a friend request already exists
#     if FriendRequest.objects.filter(
#         from_user=request.user,
#         to_user=to_user
#     ).exists():
#         messages.info(request, "Friend request already sent.")
#     else:
#         FriendRequest.objects.create(from_user=request.user, to_user=to_user)
#         messages.success(request, "Friend request sent successfully.")
    
#     return redirect(request.GET.get('next', 'user:grid'))



@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.accepted = True
        friend_request.save()
        Friend.make_friend(request.user, friend_request.from_user)
        Friend.make_friend(friend_request.from_user, request.user)
    return redirect('user:friend_requests')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('user:friend_requests')

@login_required
def view_friend_requests(request):
    incoming_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    outgoing_requests = FriendRequest.objects.filter(from_user=request.user, accepted=False)
    return render(request, 'friend_requests.html', {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})

@login_required
def friends_list(request):
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except Friend.DoesNotExist:
        friends = []

    return render(request, 'friends_list.html', {'friends': friends})



@login_required
def remove_friend(request, friend_id):
    try:
        friend = get_object_or_404(User, id=friend_id)
        friend_list = get_object_or_404(Friend, current_user=request.user)
        if friend in friend_list.users.all():
            friend_list.users.remove(friend)
            # Optionally, you might want to remove the user from the friend’s list too
            friend_list_of_friend = get_object_or_404(Friend, current_user=friend)
            if request.user in friend_list_of_friend.users.all():
                friend_list_of_friend.users.remove(request.user)
    except Friend.DoesNotExist:
        pass  # Handle the case where the user is not in any friend list

    return redirect('user:friends_list')




@login_required
def inbox_view(request):
    # Get all unique partners the user has had conversations with
    sent_messages = Message.objects.filter(sender=request.user).values('recipient').distinct()
    received_messages = Message.objects.filter(recipient=request.user).values('sender').distinct()
    
    partner_ids = set()
    for message in sent_messages:
        partner_ids.add(message['recipient'])
    for message in received_messages:
        partner_ids.add(message['sender'])
    
    partners = User.objects.filter(id__in=partner_ids)
    
    context = {
        'partners': partners,
    }
    return render(request, 'inbox.html', context)


@login_required
def send_message_view(request, user_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        recipient = get_object_or_404(User, id=user_id)
        message = Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('user:chatbox', user_id=user_id)
    else:
        pass

@login_required
def chat_view(request, user_id):
    partner = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender=request.user, recipient=partner
    ) | Message.objects.filter(
        sender=partner, recipient=request.user
    ).order_by('timestamp')
    
    context = {
        'partner': partner,
        'messages': messages
    }
    return render(request, 'chatbox.html', context)

# @login_required
# def add_to_favorites(request, profile_id):
#     profile = get_object_or_404(User, id=profile_id)
#     Favorite.objects.get_or_create(user=request.user, favorite=profile)

#     # Get the return URL from the query parameters, default to the grid page if not provided
#     next_url = request.GET.get('next', 'user:grid')
#     query_params = request.GET.get('query', '')
    
#     # If a search query exists, append it to the redirect URL
#     if query_params:
#         next_url = f"{next_url}?{urlencode({'name': query_params})}"
    
#     return redirect(next_url)


@login_required
def remove_from_favorites(request, profile_id):
    profile = get_object_or_404(User, id=profile_id)
    favorite = Favorite.objects.filter(user=request.user, favorite=profile)
    if favorite.exists():
        favorite.delete()

    # Get the return URL from the query parameters, default to the favorites page if not provided
    return_url = request.GET.get('next', 'user:favorites')
    return redirect(return_url)


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})




stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

logger = logging.getLogger(__name__)

class SubscriptionView(View):
    template_name = 'subscription.html'

    def get(self, request):
        return render(request, self.template_name, {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })

    def post(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            logger.error("Session ID not provided.")
            return redirect('user:failed')

        try:
            # Retrieve the checkout session
            session = stripe.checkout.Session.retrieve(session_id)
            # Retrieve the subscription associated with the session
            subscription = stripe.Subscription.retrieve(session.subscription)

            if not subscription:
                logger.error(f"Subscription not found for session ID: {session_id}")
                return redirect('user:failed')

            # Get product details
            product_id = subscription.items.data[0].price.product
            product = stripe.Product.retrieve(product_id)

            if not product:
                logger.error(f"Product not found for product ID: {product_id}")
                return redirect('user:failed')

            # Save subscription details to your model
            Subscription.objects.create(
                user=request.user,
                stripe_subscription_id=subscription.id,
                product_name=product.name,
                amount=subscription.items.data[0].price.unit_amount / 100  # Amount in dollars
            )

            logger.info(f"Subscription created for user {request.user.username}, subscription ID: {subscription.id}")
            return redirect('user:success')

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            return redirect('user:failed')
        except Exception as e:
            logger.error(f"General error: {e}")
            return redirect('user:failed')




@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            # Verify and construct the Stripe event
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            print(f"Constructed event: {event}")  # Print the constructed event

            if event['type'] == 'invoice.payment_succeeded':
                invoice = event['data']['object']
                print(f"Invoice: {invoice}")  # Print the invoice data

                subscription_id = invoice.get('subscription')
                customer_id = invoice.get('customer')

                if subscription_id and customer_id:
                    try:
                        # Retrieve the subscription from Stripe
                        subscription = stripe.Subscription.retrieve(subscription_id)
                        print(f"Retrieved subscription: {subscription}")  # Print the retrieved subscription

                        # Extract product name and amount from subscription items
                        subscription_items = subscription['items']['data']  # Correctly access subscription items
                        if subscription_items:
                            item = subscription_items[0]
                            plan = item['plan']
                            product_name = plan['product']  # Adjust this line to extract product details correctly
                            amount = plan['amount'] / 100  # Convert to dollars

                            print(f"Product name: {product_name}")  # Print product name
                            print(f"Amount: {amount}")  # Print amount

                            # Find the user associated with the customer ID
                            user = User.objects.filter(stripe_customer_id=customer_id).first()
                            if user:
                                # Update or create subscription in the database
                                Subscription.objects.update_or_create(
                                    user=user,
                                    stripe_subscription_id=subscription_id,
                                    defaults={
                                        'product_name': product_name,
                                        'amount': amount,
                                        'active': subscription['status'] == 'active'
                                    }
                                )
                                print(f"Updated subscription for user {user.username}, subscription ID: {subscription_id}")
                            else:
                                print(f"No user found with customer ID {customer_id}")

                        else:
                            print(f"No items found in subscription: {subscription}")

                    except stripe.error.StripeError as e:
                        print(f"Stripe error: {e}")
                        return HttpResponse(f'Stripe error: {e}', status=400)

            return HttpResponse(status=200)

        except stripe.error.SignatureVerificationError:
            print("Invalid signature")
            return HttpResponse('Invalid signature', status=400)
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f'Error: {e}', status=500)



@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            # Verify and construct the Stripe event
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            print(f"Constructed event: {event}")  # Print the constructed event

            if event['type'] == 'invoice.payment_succeeded':
                invoice = event['data']['object']
                print(f"Invoice: {invoice}")  # Print the invoice data

                subscription_id = invoice.get('subscription')
                customer_id = invoice.get('customer')
                customer_email=invoice.get("customer_email")

                if subscription_id and customer_id:
                    try:
                        # Retrieve the subscription from Stripe
                        subscription = stripe.Subscription.retrieve(subscription_id)
                        print(f"Retrieved subscription: {subscription}")  # Print the retrieved subscription

                        # Extract product name and amount from subscription items
                        subscription_items = subscription['items']['data']
                        if subscription_items:
                            item = subscription_items[0]
                            plan = item['plan']
                            product_id = plan['product']  # Extract the product ID
                            amount = plan['amount'] / 100  # Convert to dollars

                            # Retrieve the product to get the product name
                            product = stripe.Product.retrieve(product_id)
                            product_name = product['name']

                            print(f"Product name: {product_name}")  # Print product name
                            print(f"Amount: {amount}")  # Print amount

                            # Find the user associated with the customer ID
                            user = User.objects.filter(email=customer_email).first()
                            if user:
                                # Update or create subscription in the database
                                Subscription.objects.update_or_create(
                                    user=user,
                                    stripe_subscription_id=subscription_id,
                                    defaults={
                                        'product_name': product_name,
                                        'amount': amount,
                                        'active': subscription['status'] == 'active'
                                    }
                                )
                                print(f"Updated subscription for user {user.username}, subscription ID: {subscription_id}")
                            else:
                                print(f"No user found with customer ID {customer_id}")

                        else:
                            print(f"No items found in subscription: {subscription}")

                    except stripe.error.StripeError as e:
                        print(f"Stripe error: {e}")
                        return HttpResponse(f'Stripe error: {e}', status=400)

            return HttpResponse(status=200)

        except stripe.error.SignatureVerificationError:
            print("Invalid signature")
            return HttpResponse('Invalid signature', status=400)
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f'Error: {e}', status=500)


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        price_id = request.POST.get('price_id')

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='subscription',
                success_url=YOUR_DOMAIN + '/user/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return JsonResponse({'id': checkout_session.id})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class SuccessView(View):
    def get(self, request):
        session_id = request.GET.get('session_id', None)
        # Optionally process the session_id here
        return render(request, 'success.html', {'session_id': session_id})

class FailedView(View):
    def get(self, request):
        return render(request, 'failed.html')


# for the search feature

from account.models import User 



@login_required
def partner_search_view(request):
    name_query = request.GET.get('name', '').strip()
    age_query = request.GET.get('age', '').strip()
    district_query = request.GET.get('district', '').strip()
    user = request.user

    try:
        partner_preference = user.partner_preference  # Use the correct related name

        # Start with the base query for profiles
        profiles = User.objects.filter(
            age__gte=partner_preference.age_min,
            age__lte=partner_preference.age_max,
            personaldetails__caste=partner_preference.caste,
            personaldetails__religion=partner_preference.religion,
            personaldetails__height__gte=partner_preference.height_min,
            personaldetails__height__lte=partner_preference.height_max,
            personaldetails__weight__gte=partner_preference.weight_min,
            personaldetails__weight__lte=partner_preference.weight_max,
            personaldetails__income__gte=partner_preference.income_min,
            personaldetails__income__lte=partner_preference.income_max,
            gender=partner_preference.gender,
            qualification=partner_preference.qualification
        ).exclude(id=user.id).select_related('personaldetails').prefetch_related('personaldetails')

        # Apply search filters if provided
        if name_query:
            profiles = profiles.filter(
                Q(first_name__icontains=name_query) |
                Q(last_name__icontains=name_query)
            )

        if age_query:
            try:
                age_value = int(age_query)
                profiles = profiles.filter(age=age_value)
            except ValueError:
                # Handle case where age_query is not a valid integer
                profiles = profiles.none()

        if district_query:
            profiles = profiles.filter(
                personaldetails__district__icontains=district_query
            )

        return render(request, 'search_results.html', {'profiles': profiles, 'search_query': request.GET})

    except PartnerPreferance.DoesNotExist:
        return render(request, 'search_results.html', {'profiles': User.objects.none(), 'search_query': request.GET})


@login_required
def add_to_favorites(request, profile_id):
    profile = get_object_or_404(User, id=profile_id)
    Favorite.objects.get_or_create(user=request.user, favorite=profile)

    # Get the return URL from the query parameters, default to the grid page if not provided
    next_url = request.GET.get('next', 'user:grid')
    query_params = request.GET.get('query', '')
    
    # If a search query exists, append it to the redirect URL
    if query_params:
        next_url = f"{next_url}?{urlencode({'name': query_params})}"
    
    return redirect(next_url)


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    
    # Check if they are already friends
    if Friend.objects.filter(
        (Q(current_user=request.user) & Q(users=to_user)) | 
        (Q(current_user=to_user) & Q(users=request.user))
    ).exists():
        messages.info(request, "You are already friends with this user.")
        return redirect(request.GET.get('next', 'user:grid'))
    
    # Check if a friend request already exists
    if FriendRequest.objects.filter(
        from_user=request.user,
        to_user=to_user
    ).exists():
        messages.info(request, "Friend request already sent.")
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, "Friend request sent successfully.")
    
    # Get the return URL from the query parameters, default to the grid page if not provided
    next_url = request.GET.get('next', 'user:grid')
    query_params = request.GET.get('query', '')
    
    # If a search query exists, append it to the redirect URL
    if query_params:
        next_url = f"{next_url}?{urlencode({'name': query_params})}"
    
    return redirect(next_url)





@login_required
def profile_details_view(request):
    user = request.user

    # Fetch the relevant details
    incoming_requests = FriendRequest.objects.filter(to_user=user)
    outgoing_requests = FriendRequest.objects.filter(from_user=user)
    
    # Shortlisted profiles
    shortlisted_ids = Favorite.objects.filter(user=user).values_list('favorite', flat=True)
    shortlisted_profiles = User.objects.filter(id__in=shortlisted_ids)
    
    # Contacted users (union of sender and recipient)
    sent_user_ids = Message.objects.filter(sender=user).values_list('recipient', flat=True)
    received_user_ids = Message.objects.filter(recipient=user).values_list('sender', flat=True)
    contacted_user_ids = set(sent_user_ids) | set(received_user_ids)
    contacted_users = User.objects.filter(id__in=contacted_user_ids)
    
    # Messages
    messages = Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    # Hidden profiles
    # hidden_profiles = Favorite.objects.filter(user=user, hidden=True).values_list('favorite', flat=True)

    # Friends who accepted the friend request
    accepted_friends_ids = FriendRequest.objects.filter(
        from_user=user,
        accepted=True
    ).values_list('to_user', flat=True)
    friends_list = User.objects.filter(id__in=accepted_friends_ids)

    # Partners who have shortlisted the current user
    partners_shortlisting_user_ids = Favorite.objects.filter(
        favorite=user
    ).values_list('user', flat=True)
    partners_shortlisting_users = User.objects.filter(id__in=partners_shortlisting_user_ids)

    context = {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'shortlisted_profiles': shortlisted_profiles,
        'contacted_users': contacted_users,
        'messages': messages,
        # 'hidden_profiles': User.objects.filter(id__in=hidden_profiles),
        'friends': friends_list,
        'partners_shortlisting_users': partners_shortlisting_users  # Add this to the context
    }

    return render(request, 'profile_details.html', context)


@login_required
def fetch_details(request, detail_type):
    user = request.user
    data = []

    if detail_type == 'sent':
        data = list(FriendRequest.objects.filter(from_user=user).values())
    elif detail_type == 'received':
        data = list(FriendRequest.objects.filter(to_user=user).values())
    elif detail_type == 'accepted':
        data = list(FriendRequest.objects.filter(to_user=user, accepted=True).values())
    elif detail_type == 'shortlisted':
        data = list(Favorite.objects.filter(user=user).values('favorite'))
        data = list(User.objects.filter(id__in=[item['favorite'] for item in data]).values())
    elif detail_type == 'contacted':
        sent = Message.objects.filter(sender=user).values('recipient').distinct()
        received = Message.objects.filter(recipient=user).values('sender').distinct()
        user_ids = set()
        for msg in sent:
            user_ids.add(msg['recipient'])
        for msg in received:
            user_ids.add(msg['sender'])
        data = list(User.objects.filter(id__in=user_ids).values())
    elif detail_type == 'messages':
        conversations = list(Message.objects.filter(sender=user).values('recipient').distinct())
        conversations += list(Message.objects.filter(recipient=user).values('sender').distinct())
        user_ids = set([conv['recipient'] for conv in conversations] + [conv['sender'] for conv in conversations])
        data = list(User.objects.filter(id__in=user_ids).values())
    else:
        data = {'error': 'Invalid detail type'}

    return JsonResponse(data, safe=False)
