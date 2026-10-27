from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from contas.views import registrar_user_view,login_view
from Biblioteca.views import base_catalogo,base_admin,inf_livro,adcionar_livro_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/',registrar_user_view,name="cadastro"),
    path('login/',login_view,name="login"),
    path('Catalogo/',base_catalogo,name="Catalogo"),
    path('Admin_Page/',base_admin,name="admin_base"),
    path('Admin_Page/adcionar_livro.',adcionar_livro_view,name="adcionar_livro"),
    path('inf_livro/<int:livro_id>/', inf_livro, name="inf_livro"),
]
