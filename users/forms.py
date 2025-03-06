from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class UserCreationForm(CreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.display_username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = [
          'username',
          'display_username',
          'email',
          'password'
        ]
