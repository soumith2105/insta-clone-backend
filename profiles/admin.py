from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from profiles.models import UserProfile
from connections.models import Connection
from .forms import UserChangeForm, UserCreationForm


class UserProfileAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email_id', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Details', {'fields': ('username', 'email_id',)}),
        ('Personal info', {'fields': ('full_name', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_private')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email_id', 'full_name')
    ordering = ('username', 'email_id',)
    filter_horizontal = ()

# Now register the new UserAdmin...


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)
