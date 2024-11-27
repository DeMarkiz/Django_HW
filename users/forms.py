from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'avatar', 'phone_number', 'country']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data
