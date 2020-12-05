"""Posts forms"""

# Django
from django import forms

# Models
import posts.models as models


class PostForm(forms.ModelForm):
    """Posts model form."""

    class Meta:
        model = models.Post
        fields = ('user', 'profile', 'title', 'photo')
