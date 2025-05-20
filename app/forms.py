from django import forms

class SecretMessageForm(forms.Form):
    secret_message = forms.CharField(label="Enter your secret message", max_length=1000)