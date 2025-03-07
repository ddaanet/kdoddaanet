from django.urls import include, path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_done/', views.register_done, name='register_done'),
    path('edit/', views.edit, name='edit'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('logout_done/', views.logout_done, name='logout_done'),
 ]
