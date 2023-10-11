from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter password"}
        ),
    )


class RegisteringForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter username"}
        ),
    )
    email = forms.CharField(
        label="Email Address",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter password"}
        ),
    )
    confirmation = forms.CharField(
        label="Confirm password",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter password again"}
        ),
    )
