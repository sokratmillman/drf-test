from django.urls import path

from .views import LoginAPIView, RegisterAPIView

app_name = 'registration'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register_api"),
    path('login/', LoginAPIView.as_view(), name="login_api"),
]
