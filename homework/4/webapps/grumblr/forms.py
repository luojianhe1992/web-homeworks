__author__ = 'jianheluo'

from django import forms
from grumblr.models import *

# def RegistrationForm to do the registration validation job
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, label='User Name')

    first_name = forms.CharField(max_length=20, label='First name')
    last_name = forms.CharField(max_length=20, label='Last name')

    email = forms.EmailField(max_length=200)

    password1 = forms.CharField(max_length=40, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=40, label='Confirm Password', widget=forms.PasswordInput)


    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data;

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.all().filter(username = username):
            raise forms.ValidationError("Username is already taken.")

        return username


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        # exclude the user field, because the user can not edit the user
        exclude = ('user',)
        # so the field are 'first_name', 'last_name', 'age', 'short_bio'

        widgets = {'picture' : forms.FileInput() }




class Edit_Profile_Form(forms.Form):

    first_name = forms.CharField(max_length=100, label='Company', widget=forms.TextInput)
    last_name = forms.CharField(max_length=100, label='Title', widget=forms.TextInput)
    age = forms.IntegerField(min_value = 0 ,max_value=100, widget=forms.IntegerField)
    short_bio = forms.CharField(max_length=200, label='Skill', widget=forms.TextInput)

    def clean(self):

        print("call overall clean function for the Edit_Profile_Form.")

        cleaned_data = super(Edit_Profile_Form, self).clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        age = cleaned_data.get('age')
        short_bio = cleaned_data.get('short_bio')

        return cleaned_data

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        print("call clean_first_name function.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        print("call clean_last_name function.")
        return last_name

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if not isinstance(age, int):
            raise forms.ValidationError("Please enter a integer for the age.")

        print("call clean_age function.")
        return age

    def clean_short_bio(self):
        short_bio = self.cleaned_data.get('short_bio')
        print("call clean_short_bio function.")
        return short_bio



class Email_Form(forms.Form):

    email = forms.EmailField(max_length=50, label="User email:")

    def clean(self):

        cleaned_data = super(Email_Form, self).clean()

        email = cleaned_data.get('email')

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == "":
            raise forms.ValidationError("Please enter the email address.")

        return email