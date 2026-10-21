from django.contrib import admin
from django.urls import path
from contas.views import registrar_user_view,login_view
from Biblioteca.views import base_catalogo,base_admin,inf_livro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/',registrar_user_view,name="cadastro"),
    path('login/',login_view,name="login"),
    path('Catalogo/',base_catalogo,name="Catalogo"),
    path('Admin_Page/',base_admin,name="admin_base"),
    path('inf_livro/',inf_livro,name="inf_livro"),
]
