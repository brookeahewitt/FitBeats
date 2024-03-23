from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('generate', views.generate, name="generate"),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),

]