from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        if 'data' in kwargs:
            data = kwargs['data'].copy()  # Make a mutable copy of the data
            data['password1'] = data.get('password', '')  # Map 'conf-pass' to 'password2'
            data['password2'] = data.get('conf-pass', '')  # Map 'conf-pass' to 'password2'
            self.data = data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password')
    #     password2 = cleaned_data.get('password2')

    #     if password != password2:
    #         raise forms.ValidationError('Passwords do not match')