from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('generate', views.generate, name="generate"),
    path('info', views.info, name="info"),
]