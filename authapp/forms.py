from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import forms, HiddenInput
import random, hashlib
from authapp.models import ShopUser
from datetime import datetime


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.activation_key_expired = datetime.now()
        user.save()
        return user

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise forms.ValidationError("Вы слишком маленький")
        return data_age

    # def clean_email(self):
    #     data_email = self.cleaned_data['email']
    #     registered_emails = [user.email for user in ShopUser.objects.all()]
    #     for email in registered_emails:
    #         if data_email == email:
    #             raise forms.ValidationError("Пользователь с данным email уже существует")
    #     return data_email


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'password', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = HiddenInput()
