import datetime
from django import forms
from .file_dal import *
from django.core.validators import FileExtensionValidator


class LoginForm(forms.Form):
    user_email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "userEmail", 'placeholder': "example@example.com"})
    )
    user_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "userPassword", 'placeholder': "Must be 8 character long"}),
        min_length= 8,
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user_email = cleaned_data.get("user_email")
        user_pass = cleaned_data.get("user_pass")
        # user_detail = get_user_by_email(user_email)
        # for detail in user_detail:
        #     database_user_pass = detail.user_pass
        # if len(get_user_email(user_email)) < 1:
        #     msg = "Does not have an account under this email"
        #     self.add_error('user_email', msg)
        # elif get_user_email(user_email) and user_pass != database_user_pass:
        #     msg = "Enter the correct password"
        #     self.add_error('user_pass', msg)


class uploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "file_name", 'placeholder': "Input file name"}
    ))
    category = forms.CharField(widget=forms.Select(
        choices=get_category_list(),
        attrs={'class': "form-select", 'id': "category"})
    )
    issue_date = forms.DateField(initial=datetime.date.today, input_formats=['%Y-%m-%d'], widget=forms.SelectDateWidget(
        attrs={'class': "form-control form-control-sm", 'id': "issue_date", 'placeholder': "Input issue date"}
    ))
    expire_date = forms.DateField(initial=datetime.date.today, input_formats=['%Y-%m-%d'], widget=forms.SelectDateWidget(
        attrs={'class': "form-control form-control-sm", 'id': "expire_date", 'placeholder': "Input issue date"}
    ))
    file_upload = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={'class': "form-control", 'type': "file", 'placeholder': "formFile", 'accept': "application/pdf", 'onchange': "ValidateSingleInput(this)"}
    ))
