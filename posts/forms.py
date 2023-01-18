from django import forms
from . import models


class CreatePostForm(forms.ModelForm):

    def set_choices(self, groups, id="", username="", ):
        CHOICES = []
        for group in groups:
            if group.groupprofile.name == "Feed":
                if group.name == str(id) + username + str(id):
                    CHOICES.append((group.id, group.groupprofile.name))
            else:
                CHOICES.append((group.id, group.name))
        self.fields['host_group'].choices = CHOICES

    class Meta:
        model = models.Post
        fields = ['host_group', 'text', 'media']
