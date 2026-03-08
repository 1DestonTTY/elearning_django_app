from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher

#create a custom admin view for user
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles & Info', {
            'fields': ('is_student', 'is_teacher', 'real_name', 'profile_photo', 'status_update')
        }),
    )

#register it using your new CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

#register the profile models
admin.site.register(Student)
admin.site.register(Teacher)