from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, DetailView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Signinform,LoginForm,ProfileUpdateForm
from django.urls import reverse_lazy,reverse
from .models import User
from django.views import View
from typing import Any
from django.forms.forms import BaseForm
from.forms import regprofile1,employee,jobseeker
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.views import PasswordChangeView
from .forms import CustomPasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'accounts/password_change_form.html'

class LoginView(View):
    
    def get(self, request):
        context = {'form': LoginForm()}
        return render(request, 'accounts/signin.html', context)

    def post(self, request):
        context = {}
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user_from_db = User.objects.get(email=email)
                username = user_from_db.username
                user = authenticate(request, username=username, password=password)
                if not user:
                    messages.error(request, 'Invalid username or password')
                    return render(request, 'accounts/signin.html', context)

                login(request, user)
                return redirect(reverse('user:home'))

            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return render(request, 'accounts/signin.html', context)
        else:
            messages.error(request, 'Please correct the error below.')
        
        return render(request, 'accounts/signin.html', context)

def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = Signinform()
        return render(request, 'accounts/register.html', context)
    elif request.method == 'POST':
        form = Signinform(data=request.POST)
        context['form'] = form
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'accounts/register.html', context)
        try:
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('account:regprofile1')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'accounts/register.html', context)
        
class Regpro1View(LoginRequiredMixin, UpdateView):
    model = User
    form_class = regprofile1
    template_name = 'accounts/regprofile1.html'
    success_url = reverse_lazy('account:regprofile2')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})
 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

class EmployeeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = employee
    template_name = 'accounts/employee.html'
    success_url = reverse_lazy('account:relations')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})
 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
    
class JobseekerView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = jobseeker
    template_name = 'accounts/jobseeker.html'
    success_url = reverse_lazy('account:relations')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})
 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
    
        
def regprofile2(request):
    return render(request,'accounts/regprofile2.html')

def relations(request):
    return render(request,'accounts/relations.html')   



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_view.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['data'] = self.request.user
        return context
    
class ProfileUpdateView(LoginRequiredMixin, FormView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('account:profile')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        if self.request.method == 'POST':
            return form_class(self.request.POST, self.request.FILES, instance=self.request.user)
        else:
            return form_class(instance=self.request.user)
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            print(form.errors)  # Debugging: Print form errors to console
            return self.form_invalid(form)


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:profile')
        return render(request, 'accounts/change_password.html', {'form': form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('/')
    

class DeleteProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/delete_profile_confirm.html')

    def post(self, request):
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your profile has been deleted successfully.')
        return redirect('/')  # Ensure 'home' is correctly defined in your URL configurations