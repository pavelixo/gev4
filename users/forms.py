from django import forms
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control rounded-0 bg-dark text-light border border-light'
            })

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control rounded-0 bg-dark text-light border border-light'
            })



class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = [
          'username',
          'display_username',
          'email',
          'password'
        ]


class TransferForm(forms.Form):
    recipient_username = forms.CharField(
        label='Recipient Username',
        max_length=150,
        required=True
    )
    amount = forms.DecimalField(
        label='Amount',
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        required=True
    )

    def clean_recipient_username(self):
        recipient_username = self.cleaned_data.get('recipient_username')
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            raise forms.ValidationError('Recipient user does not exist.')
        return recipient
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control rounded-0 bg-dark text-light border border-light'
            })
