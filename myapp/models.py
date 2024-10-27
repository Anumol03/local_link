from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Ward(models.Model):
    ward_no = models.PositiveIntegerField()
    house_no = models.PositiveIntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_name = models.CharField(max_length=100)

    def __str__(self):
        return self.service_name


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
    description = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True,
                                    default="/profilepics/deafault.jpg")
    is_approved = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)
    cover_pic = models.ImageField(upload_to="coverpics/", blank=True, )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username




class Posts(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="postimages", null=True, blank=True)
    video = models.FileField(upload_to="postvideos", null=True, blank=True) 
    # post uploaded user
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_posts")
    created_date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(CustomUser, related_name="post_like")

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_comment")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text


class History(models.Model):
    picture = models.ImageField(upload_to='history_pics/', blank=True, null=True)  # For uploading an image
    heading = models.CharField(max_length=255)  # Title or heading of the historical event
    content = models.TextField()  # Detailed description/content
    year_start = models.PositiveIntegerField()  # Starting year
    year_end = models.PositiveIntegerField(blank=True, null=True)  # Ending year (can be blank for ongoing events)

    def __str__(self):
        return self.heading


class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="complaints")
    ward_no = models.PositiveIntegerField()  # Ward number linked to complaint
    ward_name = models.CharField(max_length=200)  # Ward name for the complaint
    text_complaint = models.TextField()  # Text complaint section
    pdf_complaint = models.FileField(upload_to="complaints_pdfs/", blank=True, null=True)  # PDF upload for complaint
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.name} in Ward {self.ward_no}"

class ComplaintReply(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="replies")
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})
    reply_text = models.TextField()
    reply_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reply by {self.admin} on {self.reply_date}"
