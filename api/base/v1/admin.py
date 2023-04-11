from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.base.forms import userModelCreationForm, userModelChangeForm
from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel


class userModelAdmin(UserAdmin):
    add_form = userModelCreationForm
    form = userModelChangeForm
    model = UserModel
    list_display = ('Email','Username', 'is_staff', 'is_active', 'date_joined','last_login')
    list_filter = ('Email','Username', 'is_staff', 'is_active', 'date_joined','last_login')
    fieldsets = (
        (None, {'fields': ('Email','Username', 'password','Permissions','Slave_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email','Username', 'password1', 'password2', 'is_staff', 'is_active','Slave_id')}
         ),
    )
    search_fields = ('Email','Username',)
    ordering = ('Email','Username',)


admin.site.register(UserModel, userModelAdmin)
admin.site.register(PermissionModel)
