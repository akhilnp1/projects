from django.forms import DateInput, Form, ModelForm, CharField, NumberInput, Select, TextInput, PasswordInput, EmailField, EmailInput,FileInput
from .models import User
from django import forms

# forms.py
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old password',
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        max_length=128,
        min_length=8,
    )
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        max_length=128,
        min_length=8,
    )
    new_password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        max_length=128,
        min_length=8,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form fields if needed
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})




class Signinform(ModelForm):
     confirm_password = CharField(
        min_length=8,
        max_length=50,
        label='Confirm Password',
        required=True,
        widget=PasswordInput({
            'class': 'form-control'
        })
        )
     
       
     class Meta:
          model=User
          fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
           
               
          ]

          widgets={
            'first_name': TextInput(attrs={'class': 'form-control','required':'required'}),
            'last_name': TextInput(attrs={'class': 'form-control','required':'required'}),
            'username': TextInput(attrs={'class': 'form-control','required':'required'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            
               
          }
     def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

     def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Password and Confirm Password do not match")

        return cleaned_data
          
       
class LoginForm(Form):
    email = EmailField(
        max_length = 50,
        min_length = 5,
        label = 'Email',
        required = True,
        widget = EmailInput({
                'class': 'form-control'
            })
    )

    password = CharField(
        max_length = 25,
        min_length = 4,
        label = 'Password',
        required = True,
        widget = PasswordInput({
                'class': 'form-control'
            })
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()

class employee(forms.ModelForm):
    class Meta:
        model=User
        fields=['company_name', 'designation', 'location']  

        widgets={
            'company_name': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
            'designation': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
            'location': forms.TextInput(attrs={'class': 'form-control','required':'required'}),

        }

class jobseeker(forms.ModelForm):
    class Meta:
        model=User
        fields=['job_title', 'expertise']  

        widgets={
            'job_title': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
            'expertise': forms.Select(attrs={'class': 'form-control','required':'required'}),

        }


class regprofile1(forms.ModelForm):

    hobbies = forms.MultipleChoiceField(
        choices=User.HOBBIES_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    interests = forms.MultipleChoiceField(
        choices=User.INTERESTS_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    age = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'readonly': 'readonly', 
            'placeholder': 'Age will be calculated automatically'
        }),
        required=False
    )
    class Meta:
        model = User
        fields = [
            'profile_photo', 'date_of_birth', 'gender', 
            'hobbies', 'interests', 'qualification','phone_number',
            'smoking_status',
            'drinking_status',
           
        ]

        widgets={
            'gender': forms.Select(attrs={'class': 'form-control','required':'required'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','required':'required'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'qualification': forms.Select(attrs={'class': 'form-control','required':'true'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'interests': forms.CheckboxSelectMultiple(attrs={'class': 'form-control','required':'required'}),
            'hobbies': forms.CheckboxSelectMultiple(attrs={'class': 'form-control','required':'required'}),
            'smoking_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'drinking_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),

          }
    def __init__(self, *args, **kwargs):
        super(regprofile1, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['age'].initial = self.instance.age 
               
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.hobbies = ','.join(self.cleaned_data['hobbies'])
        user.interests = ','.join(self.cleaned_data['interests'])
        if commit:
            user.save()
        return user
    

class ProfileUpdateForm(Signinform):
    password = None
    confirm_password = None
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'company_name',
            'designation',
            'location',
            'job_title',
            'expertise',
            'gender',
            'date_of_birth',
            'qualification',
            'profile_photo',
          
            'smoking_status',
            'drinking_status',
           
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'username': TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
            'designation': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
            'location': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise': forms.Select(attrs={'class': 'form-control'}),

            'gender': forms.Select(attrs={'class': 'form-control','required':'required'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','required':'required'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'qualification': forms.Select(attrs={'class': 'form-control','required':'true'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
           
            'smoking_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'drinking_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),


        }

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email