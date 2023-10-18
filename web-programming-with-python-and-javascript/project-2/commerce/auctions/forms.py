from django import forms

from .models import Listing, User


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"placeholder": "Enter password"}),
    )


class RegisteringForm(forms.ModelForm):
    confirmation = forms.CharField(
        label="Confirm password",
        widget=forms.TextInput(attrs={"placeholder": "Enter password again"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Enter username"}),
            "email": forms.TextInput(attrs={"placeholder": "Enter email"}),
            "password": forms.TextInput(attrs={"placeholder": "Enter password"}),
        }


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "start_bid", "image_url", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter title"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter description"}),
            "start_bid": forms.TextInput(attrs={"placeholder": "Enter bid"}),
            "image_url": forms.URLInput(attrs={"placeholder": "Enter image url"}),
        }
