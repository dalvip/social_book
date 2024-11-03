# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
# from models import CustomUser
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    USER_ROLES = [
        ('author', 'Author'),
        ('seller', 'Seller'),
    ]
    user_role = models.CharField(max_length=6, choices=USER_ROLES)  # New field for user role
    public_visibility = models.BooleanField(default=True)
    birth_year = models.IntegerField(null=True, blank=True, default=2002)
    address = models.CharField(max_length=255)
   
    
    @property
    def age(self):
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - self.birth_year

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Book Title")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='books',
        limit_choices_to={'user_role': 'author'},
        verbose_name="Author"
    )
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name="Cover Image")
    description = models.TextField(verbose_name="Book Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (USD)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True, verbose_name="Publicly Available")
    genre = models.CharField(max_length=100, blank=True, verbose_name="Genre")

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['is_public']),
            models.Index(fields=['genre']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-created_at']  # Orders by creation date, newest first
        
class UploadFile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    year_of_publication = models.IntegerField()

    def __str__(self):
        return self.title

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username