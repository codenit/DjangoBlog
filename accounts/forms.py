from django import forms
from django.contrib.auth import (
        authenticate,
        get_user_model,
        login,
        logout,
    )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_qs = User.objects.filter(username=username)

        if user_qs.count() == 0:
            raise forms.ValidationError("The user does not exist")
        else:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(UserLoginForm, self).clean()

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Enter email address: ')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    #password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password2',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        print(password, password2)

        if password and password2:
            if password != password2:
                raise forms.ValidationError("The two password fields must match.")
        return cleaned_data


