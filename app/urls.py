from django.urls import path
from app import api, views

urlpatterns = [
    # APIs
    path("secret", api.create_secret, name="create_secret"),
    path("delete/<token>", api.delete_secret, name="delete_secret"),
    
    # Views
    path("", views.home, name="home"),
    path("s/<token>", views.view_secret, name="view_secret"),
]
