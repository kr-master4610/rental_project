from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_landlord = forms.BooleanField(required=False, label="Я арендодатель")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_landlord']