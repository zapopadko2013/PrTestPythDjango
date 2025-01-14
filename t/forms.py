from django import forms
 
class UserForm(forms.Form):
    phone = forms.IntegerField()
    password = forms.CharField(required=False)