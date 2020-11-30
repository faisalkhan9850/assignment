from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()

    LOGIN_TYPE = [
        ('Gmail', 'Gmail'),
        ('Facebook', 'Facebook'),
        ('Email', 'Email'),
    ]

    Role = [
        ('Manager', 'Manager'),
        ('Employees', 'Employees'),
    ]

    username = None
    first_name = models.CharField(max_length=256, blank=True, null=True)
    lastname = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True, unique=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    company = models.CharField(max_length=256, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, blank=True, null=True, choices=Role)

    social_id = models.CharField(max_length=50, blank=True, null=True)
    login_type = models.CharField(max_length=50, blank=True, null=True, choices=LOGIN_TYPE)

    device_type = models.CharField(max_length=10, blank=True, null=True)
    device_token = models.CharField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email if self.email else "NA"
