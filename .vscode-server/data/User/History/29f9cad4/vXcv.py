from django import forms
from .models import Post
from .validators import validate_symbols

class PostForm(forms.ModelForm):
    memo = forms.CharField(max_length=80, validators=[validate_symbols])
    class Meta:
        model = Post
        fields = ['title', 'content']