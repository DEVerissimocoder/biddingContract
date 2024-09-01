from django.urls import path

from usuarios import views

app_name = "usuarios"

urlpatterns = [
    path('cadastro/', views.UserCreateView.as_view(), name="register"),
    #path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    #path('login/', views.login, name="login"),
]
