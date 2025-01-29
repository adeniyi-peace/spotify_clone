from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import CustomUser

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label="Email adresss", required=True, widget=forms.EmailInput(attrs={"placeholder":"name@domain.com"}))
    first_name = forms.CharField( max_length=50, required=True)
    last_name = forms.CharField( max_length=50, required=True)
    DOB = forms.DateField(label="Date of birth", required=True, widget=forms.DateInput(attrs={"type":"date"}))
    password2 = None

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "first_name", "last_name", "DOB"]
        widgets = {"password":forms.PasswordInput(attrs={"placeholder":"Password"})}

    
    def validate_passwords(self):
        ...


    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        try:
             password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error("password1", error)

        return password1