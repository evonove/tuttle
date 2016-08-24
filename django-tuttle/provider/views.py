from django.shortcuts import render
from django.views.generic import ListView
from github import Github
from github.Repository import Repository

from .models import Provider
# Create your views here.


class RepoListView(ListView):
    model = Provider
    queryset = Provider.objects.all()
    template_name = 'repo_list.html'

    def post(self, request):
        if request.POST.get('get_repo'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            get_repo_list(username, password)
        if request.POST.get('add_dev_key'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            repo_name = request.POST.post('repo_name')
            title = request.POST.get('title')
            key = request.POST.get('key')
            add_dev_key(username, password, repo_name, key, title)
        return super(RepoListView, self).get(request)


def get_repo_list(username, password):
    g = Github(username, password)
    for repo in g.get_user().get_repos():
        provider = Provider(repository_name=repo.name)
        for key in g.get_user().get_repo(repo.name).get_keys():
                provider = Provider(repository_name=repo.name, deploy_key=key.key, title=key.title)
        provider.save()


def add_dev_key(username, password, repo_name, key, title):
    g = Github(username, password)




