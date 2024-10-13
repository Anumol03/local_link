from django.db import models
from django.contrib.auth.models import AbstractUser

class Ward(models.Model):
    ward_no=models.PositiveIntegerField()
    house_no=models.PositiveIntegerField()
    name=models.CharField(max_length=200)

    def __str__(self) :
        return self.name
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('service', 'Service'),
        ('citizen', 'Citizen'),
    ]

    email = models.EmailField(unique=True)
    ward_no = models.CharField(max_length=10)
    house_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    adhar_no = models.CharField(max_length=12, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    description=models.CharField(max_length=200,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True,default="/profilepics/deafault.jpg")
    is_approved = models.BooleanField(default=False)
    dob=models.DateField(null=True,blank=True)
    cover_pic=models.ImageField(upload_to="coverpics/",blank=True,)

    def __str__(self):
        return self.username
    
class Posts(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="postimages",null=True,blank=True)
    # post uploaded user
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_posts")
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(CustomUser,related_name="post_like")
    

    def __str__(self):
        return self.title
    

class Comments(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment_text=models.CharField(max_length=200)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post_comment")
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text