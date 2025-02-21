from django.db import models
from user.models import User

class Voter(models.Model):
    voter_id = models.AutoField(primary_key=True)  # AutoField for an automatically incrementing ID
    full_name = models.CharField(max_length=100)  # Adjusted length for realistic full names
    middle_name = models.CharField(max_length=50, blank=True, null=True)  # Optional field
    last_name = models.CharField(max_length=50)  # Surname
    permanent_address = models.CharField(max_length=255)  # Increased length for addresses
    temporary_address = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    age = models.PositiveIntegerField()  # Ensures age cannot be negative
    dob = models.DateField()  # Date of birth
    voter_image = models.ImageField(upload_to='voter_images/', blank=True, null=True)  # Path to store uploaded images
    blood_group = models.CharField(max_length=5, blank=True, null=True)  # Short string for blood groups
    wallet_address = models.CharField(max_length=42, unique=True, blank=True, null=True)  # ✅ Ethereum wallet address
    has_voted = models.BooleanField(default=False)  # ✅ Tracks if the voter has voted
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name  # Represents the object with the full name in admin or shell
