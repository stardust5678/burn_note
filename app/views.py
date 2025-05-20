import hashlib
import json
import uuid
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from app.forms import SecretMessageForm
from app.models import SecretMessage

def home(request):
    form = SecretMessageForm()

    return render(request, "app/home.html", {"form": form})

def create_secret(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("encrypted_message")
        print(message)
        token = __save_secret_message(message)
        data = {
            "token": token
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound()

def delete_secret(request, token):
    if request.method == "DELETE":
        secret = get_object_or_404(SecretMessage, token=token)
        secret.delete()
        return HttpResponse(status=204)

def view_secret(request, token):
    encrypted_message = __get_secret_message(token)

    if encrypted_message is None:
        return HttpResponseNotFound()

    return render(request, "app/view_secret.html", {"encrypted_message": encrypted_message, "token": token})

def __save_secret_message(encrypted_message):
    unique_id = uuid.uuid4()
    token = hashlib.shake_256(str(unique_id).encode("UTF-8")).hexdigest(5)

    secret = SecretMessage.objects.create(
        token=token,
        encrypted_message=encrypted_message,
        expires_at=timezone.now() + timedelta(hours=24)
    )

    return secret.token

def __get_secret_message(token):
    secret = get_object_or_404(SecretMessage, token=token)
    
    if secret.expires_at < timezone.now():
        secret.delete()
        return None
    
    return secret.encrypted_message