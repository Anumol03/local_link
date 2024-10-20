from django import forms
from .models import *

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'description', 'profile_pic','cover_pic', 'dob']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
             "email":forms.EmailInput(attrs={"class":"form-control"}),
         
            "description":forms.TextInput(attrs={"class":"form-control"}),
            "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
            "cover_pic":forms.FileInput(attrs={"class":"form-control"}),

           
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})

        }


class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","image"]


class CoverpicForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=["cover_pic"]



