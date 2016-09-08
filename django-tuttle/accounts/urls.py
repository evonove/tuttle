from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/profile/$', views.ProfileView.as_view(), name='profile'),
]
