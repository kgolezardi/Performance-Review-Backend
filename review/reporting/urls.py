from django.urls import path

from reporting import views

app_name = 'reporting'
urlpatterns = [
    path('', views.index, name='index'),
    path('self-review/', views.self_review_overview, name='self-review'),
    path('self-review-detailed/', views.self_review_detailed, name='self-review-detailed'),
]
