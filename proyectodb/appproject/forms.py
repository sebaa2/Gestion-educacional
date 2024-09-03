from django import forms

class LoginForm(forms.Form):
    txt_username  = forms.CharField()
    txt_password =forms.CharField(widget = forms.PasswordInput)