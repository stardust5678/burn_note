from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def home(request):
    return render(
        request,
        'app/home.html'
    )

def secret_url(request, token):
    return render(
        request,
        'app/secret_url.html',
        {
            "token": token
        }
    )

def secret_message(request, token):
    # show reveal button

    # when reveal button is clicked, reveal the secret message
    secret_message = __get_secret_message(token)
    return HttpResponse(f"{secret_message}")


def __get_secret_message(token):
    # TODO
    return ""