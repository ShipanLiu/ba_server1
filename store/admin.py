from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.


class ProjectInline(admin.TabularInline):
    model = models.Project
    fields = ["name", "status", "ai_model_name", "created_at", "updated_at"]
    readonly_fields = ["name", "status", "ai_model_name", "created_at", "updated_at"]
    # can_delete = False  # Optionally disable deleting projects from here

    def ai_model_name(self, project):
        return project.ai_model.name if project.ai_model else None
    # you cannot add new image(normally in admin page, you can add new instance)
    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new images from admin inline
    def has_change_permission(self, request, obj=None):
        return False  # Prevents updating images from admin
    # disable delete(the admin won't interfere with frontend)
    # or can_delete = False  # Optionally disable deleting projects from here, same functionality
    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deleting images from admin inline


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'phone', 'email', "is_staff"]

    readonly_fields = ['id', "user", 'username', 'first_name', 'last_name', "birth_date", "email", "is_staff"]
    inlines = [ProjectInline]

    list_per_page = 10

    list_select_related = ['user']
    ordering = ['-user__is_staff']
    list_filter = ['user__is_staff']

    def first_name(self, instance):
        return instance.user.first_name

    def last_name(self, instance):
        return instance.user.last_name

    def username(self, instance):
        return instance.user.username


    def is_staff(self, instance):
        return instance.user.is_staff

    def has_change_permission(self, request, obj=None):
        return True  # Prevents updating images from admin
    # you cannot add new image(normally in admin page, you can add new instance)
    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new images from admin inline
    # disable delete(the admin won't interfere with frontend)
    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deleting images from admin inline



# for inline usage for ProductAdmin
class ImageInline(admin.TabularInline):
    model = models.Image
    fields = ["thumbnail","name", "type", "old_name", "has_result"]
    # for inline class, the readonly_fields is a must
    readonly_fields = ["thumbnail", "name", "type", "old_name", "has_result"]

    def thumbnail(self, instance):
        if instance.image_file:
            # Display the image file name with a thumbnail if possible
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', instance.image_file.url)
        return "No Image"

    # you cannot add new image(normally in admin page, you can add new instance)
    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new images from admin inline
    # disable delete(the admin won't interfere with frontend)
    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deleting images from admin inline

    def has_change_permission(self, request, obj=None):
        return False  # Prevents updating images from admin


# can create a project
# can not delete a project(won't interfere with frontend)
@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    # for list view
    list_display = ["id", 'name', 'ai_model_name', 'status', 'user_name', 'created_at', 'updated_at']

    # for detailed view
    fields = ['id', "name", "description", 'ai_model_name', 'status', 'user_name', 'created_at', 'updated_at']
    readonly_fields = ['id', 'ai_model_name', 'status', 'user_name', 'created_at', 'updated_at']
    inlines = [ImageInline]

    # list_editable = ['status'] # better not change status at backend.
    list_filter = ['customer__user__username', 'ai_model', 'created_at']
    list_per_page = 10
    list_select_related = ['ai_model', 'customer', 'customer__user']
    search_fields = ['name', 'customer__user__username']

    def ai_model_name(self, project):
        return project.ai_model.name if project.ai_model else None

    def user_name(self, project):
        return project.customer.user.username if project.customer else None

    user_name.short_description = "username"

    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deleting images from admin inline
    def has_change_permission(self, request, obj=None):
        return True  # Prevents updating images from admin
    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new images from admin inline


# a DIY Filter to change the filter displaying name in admin page
class ProjectNameFilterForImageAdmin(SimpleListFilter):
    title = 'Project Name'  # Display name for the filter
    parameter_name = 'project__name'  # URL parameter

    def lookups(self, request, model_admin):
        # Return a list of tuples (value, verbose value)
        projects = set([image.project for image in model_admin.model.objects.all() if image.project])
        return [(project.id, project.name) for project in projects]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__id=self.value())
        return queryset


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    # for list view: http://127.0.0.1:8001/admin/store/image/
    list_display = ["id", "thumbnail1", "project_name", "name", "type", "old_name", "has_result"]

    # for detailed view:  http://127.0.0.1:8001/admin/store/image/76/change/
    fields = ["id", "thumbnail2", "project_name", "name", "old_name", "type", "has_result"]
    # don't need readonly_fields, becuae change not allowed
    # readonly_fields = ["thumbnail2", "project", "name", "type", "old_name", "has_result"]

    list_per_page = 10

    # retrieve optimization
    list_select_related = ["project", "project__customer__user"]
    list_filter = [ProjectNameFilterForImageAdmin, "project__customer__user__username"]
    search_fields = ["project", "project__customer__user__username"]

    def project_name(self, instance):
        return instance.project.name

    project_name.short_description = "project"



    def thumbnail1(self, instance):
        if instance.image_file:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                instance.image_file.url)
        return "No Image"

    thumbnail1.short_description = 'Thumbnail'

    def thumbnail2(self, instance):
        if instance.image_file:
            return format_html('<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 100px; max-height: 100px;" /> (click to view)'
                '</a>',
                instance.image_file.url, instance.image_file.url)
        return "No Image"

    thumbnail2.short_description = 'Thumbnail'




    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Modify the queryset if needed, for example, to filter images based on certain criteria
        return queryset

    # Optionally, you can override methods like save_model if you want to perform additional actions when an Image is saved
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Additional actions after saving the object

    # disable delete(the admin won't interfere with frontend)
    def has_delete_permission(self, request, obj=None):
        return False  # Prevents deleting images from admin inline

    # you cannot add new image(normally in admin page, you can add new instance)
    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new images from admin inline

    def has_change_permission(self, request, obj=None):
        return False  # Prevents updating images from admin


# a DIY Filter to change the filter displaying name in admin page
class ProjectNameFilterForResultSet(SimpleListFilter):
    title = 'Project Name'  # Display name for the filter
    parameter_name = 'project__name'  # URL parameter

    def lookups(self, request, model_admin):
        # Return a list of tuples (value, verbose value)
        projects = set([resultset.project for resultset in model_admin.model.objects.all() if resultset.project])
        return [(project.id, project.name) for project in projects]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__id=self.value())
        return queryset


@admin.register(models.ResultSet)
class ResultSetAdmin(admin.ModelAdmin):
    # for list view
    list_display = ['belonged_project_id', 'belonged_project_name', "ai_model_name", "image_id", 'display_original_image', 'display_detection_image', 'display_recognition_image', 'display_interpretation_image', 'created_at', 'updated_at']

    # for detailed view
    fields = ['belonged_project_id', 'belonged_project_name', "ai_model_name", "image_id", 'display_original_image', 'display_detection_image', 'display_recognition_image', 'display_interpretation_image',
                       'created_at', 'updated_at', 'result_detection', 'result_recognition', 'result_interpretation']
    # readonly_fields = ['belonged_project_id', 'belonged_project_name', 'display_original_image', 'display_detection_image', 'display_recognition_image', 'display_interpretation_image',
    #                    'created_at', 'updated_at', 'result_detection', 'result_recognition', 'result_interpretation']

    list_per_page = 10

    list_select_related = ["project", "project__customer__user", "ai_model"]
    list_filter = [ProjectNameFilterForResultSet, "project__customer__user", 'created_at']
    search_fields = ['project__name', "project__customer__user"]

    # for list_display
    def belonged_project_name(self, instance):
        return instance.project.name

    belonged_project_name.short_description = "project name"

    def belonged_project_id(self, instance):
        return instance.project.id

    belonged_project_id.short_description = "project id"

    def image_id(self, instance):
        return instance.image.id

    def ai_model_name(self, project):
        return project.ai_model.name if project.ai_model else None


    def display_original_image(self, obj):
        if obj.image and obj.image.image_file:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />'
                '</a>',obj.image.image_file.url, obj.image.image_file.url)
        return "No Image"

    display_original_image.short_description = 'Original Image'

    def display_detection_image(self, obj):
        if obj.text_detection_image_path:
            return format_html('<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />'
                '</a>',obj.get_full_detection_image_url(), obj.get_full_detection_image_url())
        return "No Image"

    display_detection_image.short_description = 'Detection Image'

    def display_recognition_image(self, obj):
        if obj.text_recognition_image_path:
            return format_html('<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />'
                '</a>',obj.get_full_recognition_image_url(), obj.get_full_recognition_image_url())
        return "No Image"

    display_recognition_image.short_description = 'Recognition Image'

    def display_interpretation_image(self, obj):
        if obj.text_interpretation_image_path:
            return format_html('<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />'
                '</a>',obj.get_full_interpretation_image_url(), obj.get_full_interpretation_image_url())
        return "No Image"

    display_interpretation_image.short_description = 'Interpretation Image'

    def has_add_permission(self, request):
        return False  # Prevent adding new ResultSet from admin

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting ResultSet from admin

    def has_change_permission(self, request, obj=None):
        return False  # Prevent updating ResultSet from admin


@admin.register(models.AiModel)
class AiModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']


    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['created_at']

    # Optional: Customize the form used in the admin
    # fields = ['name', 'description', ...]
    # readonly_fields = ['created_at', 'updated_at']