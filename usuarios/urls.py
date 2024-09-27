from django.urls import path

from usuarios import views, views2
from django.contrib.auth.views import LoginView

app_name = "usuarios"

urlpatterns = [
    path('cadastro/', views2.cadastro, name="register"),
    path('login/', views2.login, name='login'),
    path('logout/', views2.logout, name='logout'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/add-permission/<int:pk>', views.add_permission, name='add_permission'),

]

