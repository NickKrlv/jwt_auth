from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from user.user_manager import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(verbose_name=_("email"), unique=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."),
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_query_name="custom_user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Group(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name=_("slug"),
    )
    user = models.ManyToManyField(
        CustomUser,
        through="UserGroup",
        related_name="groups_users",
        verbose_name=_("users"),
    )

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class UserGroup(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_groups",
        verbose_name=_("user"),
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="user_groups",
        verbose_name=_("group"),
    )

    class Meta:
        verbose_name = _("user group")
        verbose_name_plural = _("user groups")

    def __str__(self):
        return f"{self.user} - {self.group}"
