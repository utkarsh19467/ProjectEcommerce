from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import GuestEmail
from .forms import UserAdminCreationForm,UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import EmailActivation
User=get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin','staff','is_active')
    fieldsets = (
        (None, {'fields': ('full_name','email', 'password')}),
        #('Full_Name', {'fields': ('full_name')}),
        ('Permissions', {'fields': ('admin','staff','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)



admin.site.unregister(Group)

class EmailActivationAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model=User

admin.site.register(EmailActivation,EmailActivationAdmin)



class GuestEmailAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model=User

admin.site.register(GuestEmail,GuestEmailAdmin)
