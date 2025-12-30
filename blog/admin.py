from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, ContactMessage

# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin interface for Post model with rich text editing
    """
    list_display = ('title', 'author', 'status', 'created_on')
    list_filter = ('status', 'created_on', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model
    """
    list_display = ('post', 'author', 'approved', 'created_on')
    list_filter = ('approved', 'created_on')
    search_fields = ('content', 'author__username')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactMessage model
    """
    list_display = ('name', 'email', 'subject', 'is_resolved', 'created_on')
    list_filter = ('is_resolved', 'created_on')
    search_fields = ('name', 'email', 'subject')
