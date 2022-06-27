
from django.urls import path
from . import views #import view hiện tại của app
from .admin import admin_site

urlpatterns = [
    path('', views.index, name="index"), # khi truy vấn vào nó sẽ mở cái views index lên
    #truy cập admin site
    path('admin/', admin_site.urls)
]
