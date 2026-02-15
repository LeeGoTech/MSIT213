from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Username field
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "id": "username",
            "placeholder": "Enter your username",
            "autofocus": True,
        })

        # Password field
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "id": "password",
            "placeholder": "••••••••••••",
            "aria-describedby": "password",
        })

class CustomCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "id": "username",
            "placeholder": "Enter your username",
            "autofocus": True,
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "id": "email",
            "placeholder": "Enter your email address",
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "id": "password",
            "placeholder": "••••••••••••",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "id": "confirm_password",
            "placeholder": "••••••••••••",
        })

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")