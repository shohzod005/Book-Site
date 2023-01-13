from django.urls import path
from .views import register, logout_user, login_user

app_name = "auth"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout")
]