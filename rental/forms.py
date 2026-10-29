from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):

    ROLE_CHOICES = [
        ('customer','Customer'),
        ('supplier','Supplier')
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']