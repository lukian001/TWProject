from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ChangeUserForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    media = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
