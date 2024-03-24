from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('generate', views.generate, name="generate"),
    path('cardio', views.cardio, name="cardio"),
    path('info', views.info, name="info"),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('pilates', views.pilates, name="pilates"),
    path('yoga', views.yoga, name='yoga'),
    path('calisthenics', views.calisthenics, name='calisthenics'),
    path('stretching', views.stretching, name='stretching'),
    path('completeWorkout', views.completeWorkout, name="completeWorkout"),
    path('weightLifting', views.weight_lifting, name='weightLifting'),
    path('yoga', views.yoga, name='yoga'),
    path('calisthenics', views.calisthenics, name='calisthenics'),
    path('stretching', views.stretching, name='stretching'),
    path('pilates', views.pilates, name='pilates'),
    path('submit_workout/', views.submit_workout, name='submit_workout'),

    path('activity.html', views.activity, name='activity'),
path('playlist/', views.playlist_detail, name='playlist_detail'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)