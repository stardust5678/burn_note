from django.http import HttpResponseNotFound
from django.shortcuts import render
from app import service

from app.forms import SecretMessageForm

def home(request):
    form = SecretMessageForm()

    return render(request, "app/home.html", {"form": form})

def view_secret(request, token):
    encrypted_message = service.get_secret(token)

    if encrypted_message is None:
        return render(request, "app/not_available.html")

    return render(request, "app/view_secret.html", {"encrypted_message": encrypted_message, "token": token})