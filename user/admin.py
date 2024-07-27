from django.contrib import admin

from user.models import UserGroup, CustomUser, Group


class UserGroupInline(admin.TabularInline):
    model = UserGroup
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
    )
    inlines = [UserGroupInline]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [UserGroupInline]
