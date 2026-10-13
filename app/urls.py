from django.contrib import admin
from django.urls import path
from contas.views import registrar_user_view,login_view
from Biblioteca.views import base_catalogo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/',registrar_user_view,name="cadastro"),
    path('login/',login_view,name="login"),
    path('Catalogo/',base_catalogo,name="Catalogo"),
]
