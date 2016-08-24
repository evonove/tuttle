from django.conf.urls import url
from views import RepoListView

urlpatterns = [
    url(r'^$', RepoListView.as_view(), name='repo_list'),
]