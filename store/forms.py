from django import  forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(max_length=300, help_text="e.g: example@gmail.com",required=True)
    class Meta: # in mata we tell which model we are using

        model = User # currently we are using django own built-in user models
        fields = ('first_name','last_name','username','email','password1','password2')





