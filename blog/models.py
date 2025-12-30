from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    """
    Model representing a blog post
    """
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Published")
    )
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="blog_posts"
    )
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    featured_image = models.ImageField(
        upload_to='blog_images/', 
        blank=True, 
        null=True
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    likes = models.ManyToManyField(
        User, 
        related_name='blogpost_like', 
        blank=True
    )
    
    # Timestamps
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    def number_of_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        if self.status == 1 and not self.published_on:
            self.published_on = timezone.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Model representing comments on a blog post
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="blog_comments"
    )
    content = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)
    
    # Timestamps
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class ContactMessage(models.Model):
    """
    Model for storing contact form messages
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"