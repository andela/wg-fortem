from django.urls import path

from .views import (
    SocialLoginView
)

urlpatterns = [
    path('social_auth', SocialLoginView.as_view(), name="social_auth")
]