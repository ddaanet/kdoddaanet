from django import forms


class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
