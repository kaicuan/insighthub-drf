from django.contrib import admin
from django.utils.html import format_html
from .models import User, Dataset, Dashboard, Chart, Like, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'provider')
    ordering = ('email',)
    list_per_page = 20

    # Optional: Display profile image as a thumbnail
    def profile_image_thumbnail(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.profile_image.url)
        return "No Image"
    profile_image_thumbnail.short_description = 'Profile Image'
    readonly_fields = ('profile_image_thumbnail',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_image_thumbnail')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Provider Info', {'fields': ('provider', 'provideraccountid')}),
    )


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_at', 'columns_preview')
    search_fields = ('filename',)
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)
    list_per_page = 20

    
    def columns_preview(self, obj):
        return ", ".join(obj.columns[:5]) + ("..." if len(obj.columns) > 5 else "")
    columns_preview.short_description = 'Columns Preview'


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('is_public', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'dashboard', 'order')
    search_fields = ('title', 'description')
    list_filter = ('dashboard',)
    ordering = ('order',)
    list_per_page = 20


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'dashboard', 'created_at')
    search_fields = ('user__email', 'dashboard__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'dashboard', 'content_preview', 'created_at')
    search_fields = ('user__email', 'dashboard__title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20

    # Optional: Display content as a preview
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'