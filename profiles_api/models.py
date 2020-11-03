from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for creating user profiles, this will override the default one 
    provided by django,to support our custom user model"""

    def create_user(self, email, name, password=None):
        """ Create a new user profile.
        Default user model expects the user the model to have a username field.
        We removed user name and replace with email, we need to override default create_user(), create_superuser

        """
        if not email:
            raise ValueError('User must have an email address')
        # set to lowercase 
        email = self.normalize_email(email)
        # creates a model object
        user = self.model(email=email, name=name)
        # hashing of password
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user 


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system""" 
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    # replace default field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""  
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text