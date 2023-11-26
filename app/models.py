from datetime import timedelta
from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return "static_fldr/images/logo.png"
# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(max_length=255, verbose_name="email", unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    
    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_lable):
        return True
    
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=40, default=None)
    description = models.TextField(default=None)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,related_name="Task")
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=60))
    creation_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    comments = models.TextField(blank=True, default=None)
    taskName = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f'Task - {self.taskName}, description -  {self.comments}'
    
class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
class AdminNotification(models.Model):
    message = models.TextField()
    
    def __str__(self):
        return self.message
    
class AdditionInformationForUser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    skills = models.TextField(blank=True, null=True)
    short_info = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    facebook_link = models.CharField(max_length=255,blank=True, null=True)
    instagram_link = models.CharField(max_length=255,blank=True, null=True)
    github_link = models.CharField(max_length=255,blank=True, null=True)
    linked_in = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return str(self.user)
    