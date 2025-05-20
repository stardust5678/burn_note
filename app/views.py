from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from app.forms import SecretMessageForm

def home(request):
    form = SecretMessageForm()

    return render(request, "app/home.html", {"form": form})

def create_secret(request):
    if request.method == "POST":
        form = SecretMessageForm(request.POST)
        secret_message = form.data["secret_message"]
        encrypted_message = __encrypt_secret_message(secret_message)
        token = __save_secret_message(encrypted_message)
        return HttpResponseRedirect(f"/created/{token}")
    else:
        return HttpResponseNotFound()

def secret_url(request, token):
    if __is_valid_token(token):
        secret_url = f"http://127.0.0.1:8000/s/{token}" # TODO: productionize
        return render(
            request,
            'app/secret_url.html',
            {
                "secret_url": secret_url
            }
        )
    return HttpResponseNotFound()


def secret_message(request, token):
    if __is_valid_token(token):
        # TODO: show reveal button
        # on click, reveal secret
        secret_message = __get_secret_message(token)
        return render(request, "app/secret_message.html", {"secret_message": secret_message})
    return HttpResponseNotFound()

def reveal_secret(request, token):
    secret_message = __get_secret_message(token)
    return HttpResponse(f"{secret_message}")


def __encrypt_secret_message(secret_message):
    # TODO
    return "mockEncryptedMessage"  # Replace with actual encryption logic

def __decode_secret_message(encrypted_message):
    # TODO
    return "secret message placeholder"

def __is_valid_token(token):
    # TODO
    # if secret exists and is not expired
    return True  # Replace with actual token validation logic

def __save_secret_message(encrypted_message):
    # TODO
    return "mockToken"  # Replace with actual token generation logic

def __get_secret_message(token):
    # TODO
    # fetch encrypted message from db
    encrypted_message = "mockEncryptedMessage"  # Replace with actual fetch logic
    return __decode_secret_message(encrypted_message)

def __delete_secret_message(token):
    # TODO
    return True  # Replace with actual deletion logic