from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, password_validation, PasswordResetForm, SetPasswordForm 
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Customer, Order


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password(again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
class Meta:
 model = User
 fields = ['username','email','password1','password2']
 labels = {'email': 'Email'}
 widget= {'username':forms.TextInput(attrs={'class':'form-control'})}
 
 
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  
class LoginForm(AuthenticationForm ):
     usern = UsernameField(widget=forms.TextInput(attrs={'autofucus':True, 'class':'form-control'}))
     password : forms.CharField(label=_("password"), strip=False, widget =forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MypasswordChangeForm(PasswordChangeForm):
    old_password: forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True, 'class':'form-control'}))
    new_password1: forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password1', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password2', 'class':'form-control'}))
    
class MypasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))
    
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode',]
        widgets ={'name': forms.TextInput(attrs=
        {'class': 'form-control'}), 'locality': forms.TextInput(attrs=
        {'class': 'form-control'}), 'city': forms.TextInput(attrs=
        {'class': 'form-control'}), 'state': forms.Select(attrs=
        {'class': 'form-control'}), 'zipcode': forms.NumberInput(attrs=
        {'class':'form-control'})}                                                     
        

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', ]   