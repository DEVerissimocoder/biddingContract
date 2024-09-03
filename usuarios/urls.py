from django.urls import path

from usuarios import views
from django.contrib.auth.views import LoginView

app_name = "usuarios"

urlpatterns = [
    path('cadastro/', views.UserCreateView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

