from django import forms
from .models import Followers

class LoginForm(forms.Form):
    Username = forms.CharField(max_length=120)
    Password = forms.CharField(max_length=120)


class WelcomePage(forms.Form):
    celeb_user_name = forms.CharField(widget=forms.Textarea)
    #celeb_followers = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    celeb_followers = forms.CharField(max_length=300, required=False)

    hash_tag = forms.CharField(max_length=120)

    hash_tag_users = forms.CharField(max_length=300, required=False)
