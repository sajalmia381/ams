from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserCustomAdmin(UserAdmin):

    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    search_fields = ['email', 'full_name', 'admin', 'staff', 'is_active']
    list_display = ['email', 'admin', 'staff', 'is_active']
    list_filter = ['admin', 'staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Username', {
            'classes': ('collapse',),
            'fields': ('username',)
        }),
        ('User Details', {'fields': ('full_name', 'bio', 'image',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            # 'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    ordering = ('email',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        obj.username = obj.email.split('@')[0]
        super().save_model(request, obj, form, change)


admin.site.register(User, UserCustomAdmin)

