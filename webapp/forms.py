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


class LoginUserForm(forms.Form):
    email = forms.EmailField(label="Email",required=True, widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    
    
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)


    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email_field.verbose_name},
        )
    

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