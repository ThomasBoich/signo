from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile, Vizit, MedCard, Action


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'last_name', 'first_name', 'patronymic', 'uniq_id', 'pasport_series', 'pasport_number', 'phone', 'date_of_birthday', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_name', 'first_name', 'patronymic', 'pasport_series', 'pasport_number', 'phone', 'date_of_birthday', 'addres', 'photo',)}),
        ('Permissions', {'fields': ('is_superuser', 'ban', 'ban_date', 'type', 'is_staff', 'is_active', 'groups','user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'ban','type', 'first_name', 'last_name', 'patronymic', 'pasport_series', 'pasport_number', 'phone', 'addres')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('id',)


# class MedCardAdmin(admin.ModelAdmin):
#     save_as = True
#     list_display = ['user', 'age', 'height', 'blood', 'weight']
#     search_fields = ['user', 'age', 'height', 'blood', 'weight']
#     readonly_fields = ['user']
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     save_as = True
#     list_display = ['user']
#     search_fields = ['user']
#     readonly_fields = ['user']


# class ActionAdmin(admin.ModelAdmin):
#     readonly_fields = ['id', 'pub_date']


# admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Vizit)
# admin.site.register(MedCard, MedCardAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Action, ActionAdmin)