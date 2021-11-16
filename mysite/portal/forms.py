import datetime
from django import forms
from .file_dal import *
from .account_dal import *
from .encryption_utility import *
from datetime import date
from bootstrap_datepicker_plus import DatePickerInput
from django.core.validators import FileExtensionValidator


class LoginForm(forms.Form):
    user_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "userId", 'placeholder': "Input your user ID"}),
        max_length = 20,
    )
    user_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "userPassword", 'placeholder': "Must be 8 character long"}),
        min_length= 8,
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': "form-check-input", 'id': "rememberMe"}),
    )
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user_id = cleaned_data.get("user_id")
        user_pass = cleaned_data.get("user_pass")
        user_detail = get_user_by_id(user_id)
        today = date.today().strftime('%Y-%m-%d')
        for detail in user_detail:
            database_user_pass = decrypt(detail.password)
            database_active_status = detail.status
            valid_from_date = date.strftime(detail.valid_from, '%Y-%m-%d')
            valid_to_date = date.strftime(detail.valid_to, '%Y-%m-%d')
        if len(user_detail) < 1:
            msg = "Does not have any account under this USER ID!"
            self.add_error('user_id', msg)
        elif get_user_by_id(user_id) and user_pass != database_user_pass:
            msg = "Enter the correct password!"
            self.add_error('user_pass', msg)
        elif today > valid_to_date or today < valid_from_date:
            msg = "User is not valid! User valid from "+ valid_from_date + " to " +valid_to_date
            self.add_error('user_id', msg)
        elif database_active_status == 0:
            msg = "User inactivated!"
            self.add_error('user_id', msg)


class uploadForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "file_name", 'placeholder': "Input file name"}
    ))
    category = forms.CharField(widget=forms.Select(
        choices=get_category_list(),
        attrs={'class': "form-select", 'id': "category"})
    )
    # issue_date = forms.DateField(initial=datetime.date.today, input_formats=['%Y-%m-%d'], widget=DatePickerInput(
    #     format='%Y-%m-%d',
    #     attrs={'id': "issue_date", 'placeholder': "Input issue date"}
    # ))
    # expire_date = forms.DateField(initial=datetime.date.today, input_formats=['%Y-%m-%d'], widget=DatePickerInput(
    #     format='%Y-%m-%d',
    #     attrs={'id': "expire_date", 'placeholder': "Input expiration date"}
    # ))
    file_upload = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={'class': "form-control", 'type': "file", 'placeholder': "formFile", 'accept': "application/pdf", 'onchange': "ValidateSingleInput(this)"}
    ))

class adduserForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "userId", 'placeholder': "Input user ID"}))
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "userName", 'placeholder': "Input full name"}))
    person_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "personID", 'placeholder': "Input person ID"}))
    user_email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "userEmail", 'placeholder': "example@example.com"}))
    user_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control ", 'id': "userPassword", 'placeholder': "Must be between 8 to 12 characters"}), min_length=8, max_length=12)
    active_status= forms.CharField(widget=forms.Select(
        choices=get_active_status_list(),
        attrs={'class': "form-select", 'id': "activeStatus"})
    )
    user_level = forms.CharField(widget=forms.Select(
        choices=get_user_level_list(),
        attrs={'class': "form-select", 'id': "userLevel"})
    )

    def clean(self):
        cleaned_data = super(adduserForm, self).clean()
        user_id = cleaned_data.get("user_id")
        person_id = cleaned_data.get("person_id")
        if len(get_user_by_id(user_id)) >= 1:
            msg = "Already have an account under this USER ID!"
            self.add_error('user_id', msg)
        elif len(get_user_by_person_id(person_id)) >= 1:
            msg = "Already have an account under this IFIC ID"
            self.add_error('person_id', msg)

class edituserForm(forms.Form):

    user_id = forms.CharField(
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "userName", 'placeholder': "User ID"}))

    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "userName", 'placeholder': "Full name"}))

    person_id = forms.CharField(
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'class': "form-control", 'id': "personID", 'placeholder': "Person ID"}))

    user_email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "userEmail", 'placeholder': "Email"}))
    # user_pass = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': "form-control text-muted", 'id': "userPassword", 'placeholder': "Must be 8 character long"}), min_length=8)
    active_status= forms.CharField(widget=forms.Select(
        choices=get_active_status_list(),
        attrs={'class': "form-select", 'id': "activeStatus"})
    )
    user_level = forms.CharField(widget=forms.Select(
        choices=get_user_level_list(),
        attrs={'class': "form-select", 'id': "userLevel"})
    )

    def clean(self):
        cleaned_data = super(edituserForm, self).clean()


class ChangePassForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(ChangePassForm, self).__init__(*args, **kwargs)

    old_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "oldPassword", 'placeholder': "Input previous password"}))
    new_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "newPassword", 'placeholder': "Input new password. Length between 8 and 12"}),
        min_length=8, max_length=12,
    )
    conf_pass = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "confPassword", 'placeholder': "Repeat password. Length between 8 and 12"}),
        min_length=8, max_length=12,
    )

    def clean(self):
        cleaned_data = super(ChangePassForm, self).clean()
        old_pass = cleaned_data.get("old_pass")
        new_pass = cleaned_data.get("new_pass")
        conf_pass = cleaned_data.get("conf_pass")
        user_id = self.user_id
        user_detail = get_user_by_id(user_id)
        for detail in user_detail:
            database_pass = decrypt(detail.password)
        if old_pass != database_pass:
            msg = "Password not matched!"
            self.add_error('old_pass', msg)
        elif new_pass != conf_pass:
            msg = "Correctly repeat the password!"
            self.add_error('conf_pass', msg)