from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("secret", views.create_secret, name="create_secret"),
    path("s/<token>", views.view_secret, name="view_secret"),
    path("delete/<token>", views.delete_secret, name="delete_secret")
]
