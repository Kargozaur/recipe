from django.urls import path

from .views import RegistrationApiView, LoginAPIView

app_name = "authentication"
urlpatterns = [
    path("users/", RegistrationApiView.as_view()),
    path("users/login/", LoginAPIView.as_view()),
]
