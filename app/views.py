from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from app.forms import SecretMessageForm

def home(request):
    form = SecretMessageForm()

    return render(request, "app/home.html", {"form": form})

def create_secret(request):
    if request.method == "POST":
        form = SecretMessageForm(request.POST)
        return HttpResponseRedirect("/created")
    else:
        return HttpResponseNotFound()

def secret_url(request, token):
    return render(
        request,
        'app/secret_url.html',
        {
            "token": token
        }
    )

def secret_message(request, token):
    # check if secret exists
    if token == "valid_token":  # Replace with actual token check
        # if exsits, show reveal button
        return render(request, "app/secret_message.html", {"token": token})
    # else, return 404
    return HttpResponseNotFound()

def reveal_secret(request, token):
    secret_message = __get_secret_message(token)
    return HttpResponse(f"{secret_message}")

def __get_secret_message(token):
    # TODO
    return ""