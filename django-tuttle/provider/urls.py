from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^deploy-key-list/$', views.DeployKeyListView.as_view(), name='deploykey_list'),
    url(r'^repository-list/$', views.RepositoryListView.as_view(), name='repo_list'),
]
