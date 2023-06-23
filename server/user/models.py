from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError("Email is required")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )

        user.first_name = kwargs.get('first_name')
        user.last_name = kwargs.get('last_name')
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return


class User(AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False, null=False, default='Default first name')
    last_name = models.CharField(max_length=50, blank=False, null=False, default='Default last name')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', default='media/profile/avatar.png')
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} Profile'

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
