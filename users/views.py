from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import UserAuthenticationForm, UserCreationForm
from .models import User


class LoginView(FormView):
    template_name = 'login.html'
    form_class = UserAuthenticationForm
    success_url = reverse_lazy('root-view')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.success_url)


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('root-view')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response