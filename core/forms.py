from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Contact
User = get_user_model()



class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField( widget = forms.PasswordInput(attrs={'placeholder':'Confirm password', 'id':'conf-pass'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','confirm_password')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'required':'required',
                'id':'first-name',
                'placeholder':('First name')
            }),
            'last_name': forms.TextInput(attrs={
                'required':'required',
                'id':'last-name',
                'placeholder':('Last name')
            }),
            'email': forms.EmailInput(attrs={
                'id':'email',
                'placeholder':('Email')
            }),
            'password': forms.PasswordInput(attrs={
                'id':'pass',
                'placeholder':('Password')
            })
        }

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()
    
# class ContactForm(forms.ModelForm):

#     class Meta:
#         model = Contact
        
#         fields = {
#             'full_name',
#             'email',
#             'reason',
#             'message',
#         }

#         widgets = {
#             'full_name' : forms.TextInput(attrs={
#                 'class' : 'form-control',
#                 'placeholder' : ('Enter Your Name')
#             }),
#             'email' : forms.EmailInput(attrs={
#                 'class' : 'form-control',
#                 'placeholder' : ('Enter Your E-mail')
#             }),
#             'reason' : forms.TextInput(attrs={
#                 'class' : 'form-control',
#                 'placeholder' : ('Enter Your Name')
#             }),
#             'message' : forms.Textarea(attrs={
#                 'class' : 'form-control',
#                 'placeholder' : ('Write Your Message')
#             })

#         }
