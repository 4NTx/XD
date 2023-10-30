from django.urls import path
from . import views

urlpatterns = [
    path('criar_repositorios/', views.criar_repositorios, name='criar_repositorios'),
]
