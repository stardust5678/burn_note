from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("secret", views.create_secret, name="create_secret"),
    path("created/<token>", views.secret_url, name="secret_url"),
    path("s/<token>", views.secret_message, name="secret_message")
]
