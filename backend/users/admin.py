from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserActivity


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 
                   'user_type', 'soro_score', 'risk_level', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 
                                     'date_of_birth', 'bvn', 'nin')}),
        ('Contact Info', {'fields': ('address', 'state', 'lga', 
                                    'whatsapp_number', 'prefers_voice')}),
        ('Insurance Info', {'fields': ('user_type', 'soro_score', 
                                      'total_claims', 'approved_claims', 
                                      'rejected_claims')}),
        ('Bank Info', {'fields': ('bank_account_number', 'bank_name', 
                                 'account_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'first_name', 'last_name',
                      'password1', 'password2', 'user_type'),
        }),
    )
    
    inlines = [UserProfileInline]


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__phone_number', 'user__email', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)