from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


UserModel = get_user_model()

class CreateUserForm(forms.ModelForm):
    # email = forms.EmailField(label="Email adresss", required=True, widget=forms.EmailInput(attrs={"placeholder":"name@domain.com"}))
    # first_name = forms.CharField( max_length=50, required=True)
    # last_name = forms.CharField( max_length=50, required=True)
    # DOB = forms.DateField(label="Date of birth", required=True, widget=forms.DateInput(attrs={"type":"date"}))
    # password1 = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={"placeholder":"Password"})) 
    

    class Meta:
        model = CustomUser
        fields = ["email", "password", "name", "DOB"]
        widgets = {"email":forms.EmailInput(attrs={"placeholder":"name@domain.com"}),
                   "password":forms.PasswordInput(attrs={"placeholder":"Password"}),
                   "DOB":forms.DateInput(attrs={"type":"date"})}
        labels = {"email":"Email adresss", "DOB":"Date of birth"}
        help_texts = {"password":password_validation.password_validators_help_text_html()}
        errors = {"password":{"required":"Password cannot be Empty"},
                  "email":{"invalid":"Please enter a valid email address", "required":"Enter an email address"}}
        
    def clean_password(self):
        password = self.cleaned_data.get("password")

        try:
             password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error("password", error)

        return password


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label="Email",required=True, widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    
    

# strictly used for the admin
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

# strictly used for the admin
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)