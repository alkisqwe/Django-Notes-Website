from django.urls import path
from .views import SignUpView, password_reset_view

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_reset/", password_reset_view, name="password_reset"),
]
