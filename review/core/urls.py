from django.urls import include
from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.overview, name='overview'),
    path('criteria', views.criteria, name='criteria'),
    path('projects', views.projects, name='projects'),
]
