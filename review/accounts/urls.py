from django.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = 'accounts'
urlpatterns = [
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('core:overview')),
         name='password_change'),
    path('', include('django.contrib.auth.urls')),
]
