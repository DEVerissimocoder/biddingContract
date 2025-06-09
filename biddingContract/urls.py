from django.contrib import admin
from django.urls import path, include
from usuarios import views2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('usuarios/login/', views2.login, name='login'),
    path('', include('biddingContracts.urls')),
    path('', include('usuarios.urls')), #url do app usuarios
]
