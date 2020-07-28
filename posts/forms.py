from django import forms
from .models import PostFeed


class PostFeedForm(forms.ModelForm):

    class Meta:
        model = PostFeed
        fields = ['caption']