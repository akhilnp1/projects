from django.urls import path
from . import views
from .views import *
from .views import CustomPasswordChangeView


app_name = 'account'


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('regprofile1/', Regpro1View.as_view(), name='regprofile1'),
    path('regprofile2/', views.regprofile2, name='regprofile2'),

    path('employee/', EmployeeView.as_view(), name='employee'),
    path('jobseeker/', JobseekerView.as_view(), name='jobseeker'),

    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', TemplateView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),


     
    path('relations/', views.relations, name='relations'),


    path('delete-profile/', DeleteProfileView.as_view(), name='delete_profile'),



]
