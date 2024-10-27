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
        fields=["title","image",'video']


class CoverpicForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=["cover_pic"]

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['ward_no', 'ward_name', 'text_complaint', 'pdf_complaint']
        widgets = {
            'ward_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Select Ward Number'}),
            'ward_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Ward Name'}),
            'text_complaint': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your complaint here', 'rows': 4}),
            'pdf_complaint': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ComplaintReplyForm(forms.ModelForm):
    class Meta:
        model = ComplaintReply
        fields = ['reply_text']
        widgets = {
            'reply_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your reply here',
                'rows': 4,
            }),
        }



