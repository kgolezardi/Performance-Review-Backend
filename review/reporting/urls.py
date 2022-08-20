from django.urls import path

from reporting import views

app_name = 'reporting'
urlpatterns = [
    path('', views.index, name='index'),
    path('self-review/', views.self_review_overview, name='self-review'),
    path('self-review-detailed/', views.self_review_detailed, name='self-review-detailed'),
    path('manager-adjustment/', views.manager_adjustment, name='manager-adjustment'),
    path('peer-review/', views.peer_review_overview, name='peer-review'),
    path('peer-review-detailed/', views.peer_review_detailed, name='peer-review-detailed'),
    path('manager-review/', views.manager_review, name='manager-review'),
]
