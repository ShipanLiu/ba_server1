from django.core.validators import MinValueValidator
from django.db import models
from .utility.utilities import project_image_directory_path
from django.conf import settings
from django.contrib import admin

# Create your models here.

# AI Model
class Model(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"ai-mode id: {self.id}, name: {self.name}"

    class Meta:
        db_table = "model"



class Project(models.Model):

    # 'PENDING' will be saved in database, 'Pending' is just for human reading
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    ai_model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, related_name='projects')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')  # Example: pending, processing, completed, failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"project id: {self.id}, name: {self.name}"

    class Meta:
        db_table = "project"

class Image(models.Model):
    # if project is deleted, then all the images should be deleted
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=200)
    image_file = models.ImageField(upload_to=project_image_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"image id: {self.id}, name: {self.name}, belonged project: {self.project}"

    class Meta:
        db_table = "image"

class ResultSet(models.Model):
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name="result_set")
    result_detection = models.JSONField()
    result_recognition = models.JSONField()
    result_interpretation = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"result_set id: {self.id}"

    class Meta:
        db_table = "result_set"




# here define the profile
class Customer(models.Model):
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    def email(self):
        return self.user.email

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
