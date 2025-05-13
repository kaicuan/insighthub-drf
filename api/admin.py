from django.contrib import admin
from django.utils.html import format_html
from .models import User, Dataset, Dashboard, Chart, Like, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_archived', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_archived', 'is_superuser', 'provider')
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

    actions = ['archive_users', 'unarchive_users']

    def archive_users(self, request, queryset):
        queryset.update(is_archived=True)
    archive_users.short_description = "Archive selected users"

    def unarchive_users(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_users.short_description = "Unarchive selected users"


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'is_archived', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('is_public', 'is_archived', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20

    actions = ['archive_dashboards', 'unarchive_dashboards']

    def archive_dashboards(self, request, queryset):
        queryset.update(is_archived=True)
    archive_dashboards.short_description = "Archive selected dashboards"

    def unarchive_dashboards(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_dashboards.short_description = "Unarchive selected dashboards"


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_at', 'is_archived', 'columns_preview')
    search_fields = ('filename',)
    list_filter = ('uploaded_at', 'is_archived')
    ordering = ('-uploaded_at',)
    list_per_page = 20

    
    def columns_preview(self, obj):
        return ", ".join(obj.columns[:5]) + ("..." if len(obj.columns) > 5 else "")
    columns_preview.short_description = 'Columns Preview'

    actions = ['archive_datasets', 'unarchive_datasets']

    def archive_datasets(self, request, queryset):
        queryset.update(is_archived=True)
    archive_datasets.short_description = "Archive selected datasets"

    def unarchive_datasets(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_datasets.short_description = "Unarchive selected datasets"


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'dashboard', 'is_archived',)
    search_fields = ('title', 'description')
    list_filter = ('dashboard', 'is_archived')
    ordering = ('order',)
    list_per_page = 20
    
    actions = ['archive_charts', 'unarchive_charts']

    def archive_charts(self, request, queryset):
        queryset.update(is_archived=True)
    archive_charts.short_description = "Archive selected charts"

    def unarchive_charts(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_charts.short_description = "Unarchive selected charts"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'dashboard', 'created_at', 'is_archived')
    search_fields = ('user__email', 'dashboard__title')
    list_filter = ('created_at', 'is_archived')
    ordering = ('-created_at',)
    list_per_page = 20

    actions = ['archive_likes', 'unarchive_likes']

    def archive_likes(self, request, queryset):
        queryset.update(is_archived=True)
    archive_likes.short_description = "Archive selected likes"

    def unarchive_likes(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_likes.short_description = "Unarchive selected likes"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'dashboard', 'content_preview', 'created_at', 'is_archived')
    search_fields = ('user__email', 'dashboard__title', 'content')
    list_filter = ('created_at', 'is_archived')
    ordering = ('-created_at',)
    list_per_page = 20

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

    actions = ['archive_comments', 'unarchive_comments']

    def archive_comments(self, request, queryset):
        queryset.update(is_archived=True)
    archive_comments.short_description = "Archive selected comments"

    def unarchive_comments(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_comments.short_description = "Unarchive selected comments"
