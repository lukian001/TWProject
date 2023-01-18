from django import forms
from django.contrib.auth.models import Group


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ChangeGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    media = forms.ImageField()

    class Meta:
        model = Group
        fields = ['name']
