from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('generate', views.generate, name="generate"),
    path('cardio', views.cardio, name="cardio"),
    path('weight_lifting', views.weight_lifting, name="weight_lifting")
]