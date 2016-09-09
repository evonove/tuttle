from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from provider.models import DeployKey, Repository


class DeployKeyListView(LoginRequiredMixin, ListView):
    model = DeployKey
    template_name = 'templates/deploykey_list.html'

    def get_queryset(self):
        return DeployKey.objects.filter(repository__user=self.request.user)


class RepositoryListView(LoginRequiredMixin, ListView):
    model = Repository
    template_name = 'templates/repository_list.html'

    def get_queryset(self):
        return Repository.objects.filter(user=self.request.user)
