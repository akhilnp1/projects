from django.forms import DateInput, Form, ModelForm, CharField, NumberInput, Select, TextInput, PasswordInput, EmailField, EmailInput,FileInput
from django.contrib.auth.models import User
from django import forms
from .models import PersonalDetails,PartnerPreferance
from .models import Message



class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model=PersonalDetails
        fields=['fathers_name', 'fathers_job', 'mothers_name','mothers_job','siblings','permanent_address','present_address','country','state','district',
                'income', 'height', 'weight','caste','religion','horriscope']  

        widgets={
            'fathers_name': forms.TextInput(attrs={'class': 'form-control','required':'true'}),
            'fathers_job': forms.TextInput(attrs={'class': 'form-control','required':'true'}),
            'mothers_name': forms.TextInput(attrs={'class': 'form-control','required':'true'}),
            'mothers_job': forms.TextInput(attrs={'class': 'form-control','required':'true'}),
            'siblings': forms.NumberInput(attrs={'class': 'form-control','required':'true'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control','required':'true','rows':'3'}),
            'present_address': forms.Textarea(attrs={'class': 'form-control','required':'true','rows':'3'}),
            'country': forms.Select(attrs={'class': 'form-control','required':'true'}),
            'state': forms.Select(attrs={'class': 'form-control','required':'true'}),
            'district': forms.Select(attrs={'class': 'form-control','required':'true'}),
            'income': forms.NumberInput(attrs={'class': 'form-control','required':'true'}),
            'height': forms.NumberInput(attrs={'class': 'form-control','required':'true'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control','required':'true'}),
            'caste': forms.Select(attrs={'class': 'form-control','required':'true','placeholder':'Select'}),
            'religion': forms.Select(attrs={'class': 'form-control','required':'true','placeholder':'Select'}),
            'horriscope': forms.FileInput(attrs={'class': 'form-control','required':'true'}),

        }

        
# class partnerpreferance(forms.ModelForm):
#     class Meta:
#         model=PartnerPreferance
#         fields=['age', 'caste', 'religion','height','weight','income']  

#         widgets={
#             'age': forms.TextInput(attrs={'class': 'form-control'}),
#             'caste': forms.TextInput(attrs={'class': 'form-control'}),
#             'religion': forms.TextInput(attrs={'class': 'form-control'}),
#             'height': forms.TextInput(attrs={'class': 'form-control'}),
#             'weight': forms.TextInput(attrs={'class': 'form-control'}),
#             'income': forms.TextInput(attrs={'class': 'form-control'}),
#         }


class PartnerPreferanceForm(forms.ModelForm):
    class Meta:
        model = PartnerPreferance
        fields = [
            'age_min', 'age_max', 'caste', 'religion', 'height_min', 
            'height_max', 'weight_min', 'weight_max', 'income_min', 'income_max', 
            'qualification','gender',
        ]
        widgets = {
            'age_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'height_min': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'height_max': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'weight_min': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'weight_max': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'income_min': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'income_max': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'qualification': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
