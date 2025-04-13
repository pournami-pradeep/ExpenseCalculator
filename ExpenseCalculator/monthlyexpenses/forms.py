from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
          super(UserRegistrationForm, self).__init__(*args, **kwargs)
          self.fields['username'].widget.attrs.update({'autocomplete': 'username'})
          self.fields['email'].widget.attrs.update({'autocomplete': 'email'})
          self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
   
    first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'register','placeholder':'First Name','autocomplete':'off'}))
    last_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'register','placeholder':'Last Name','autocomplete':'off'}))
    password1 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'register','placeholder':'Password','autocomplete':'off'}))
    password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'register','placeholder':'Confirm Password','autocomplete':'off'}))
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'register','placeholder':'Username','autocomplete':'off'}))
    email = forms.EmailField(max_length=50,widget=forms.EmailInput(attrs={'class':'register','placeholder':'Email','autocomplete':'off'}))
    class Meta:
        model = User
        fields = ("first_name","last_name","username", "email", "password1", "password2")




