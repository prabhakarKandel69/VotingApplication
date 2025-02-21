from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        """
        Create and return a regular user with the given phone and password.
        """
        if not phone:
            raise ValueError("The Phone Number field is required.")
        extra_fields.setdefault('is_active', True)

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        Create and return a superuser with the given phone and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model where phone number is the unique identifier
    instead of usernames.
    """
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    citizenship_no = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    

    # Permissions and status fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamp fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'  # Phone is the unique identifier
    REQUIRED_FIELDS = []  # No additional required fields for creating superusers

    def __str__(self):
        return self.phone
