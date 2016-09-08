from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'deploykey_list'
    template_name = 'registration/profile.html'
