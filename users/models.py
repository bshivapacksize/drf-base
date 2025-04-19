import os
import uuid
import pytz

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.functional import cached_property

# from django_q.tasks import async_task

from commons.fields import TimeZoneField
from commons.models import BaseModel, TimeStampModel, UUIDBaseModel

from .manager import UserManager
from users.utils import send_password_change_email


def get_profile_picture_upload_path(_, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("user/profile-pictures/", filename)


def get_cover_image_upload_path(_, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("user/cover-image/", filename)


def get_custom_group_image_path(_, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("user/group-image/", filename)


class User(TimeStampModel, AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.UUIDField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        default=uuid.uuid4,
    )
    email = models.EmailField(
        max_length=45,
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    first_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45)
    profile_picture = models.ImageField(
        upload_to=get_profile_picture_upload_path, null=True, blank=True
    )
    cover_image = models.ImageField(
        upload_to=get_cover_image_upload_path, null=True, blank=True
    )
    time_zone = TimeZoneField(
        default="Asia/Kathmandu",
        choices=[(tz, tz) for tz in pytz.all_timezones],
        max_length=70,
    )

    # last login seems important because, last_activity can only be obtained from AuthToken class
    # if the user deletes all his session , then even this last_activity information is lost
    last_login = models.DateTimeField("last login", blank=True, null=True)
    last_activity = models.DateTimeField("last activity", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)

    failed_login_count = models.IntegerField(default=0)
    last_failed_login_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=14, null=True, blank=True)
    is_online = models.BooleanField(null=True, blank=True)
    last_online = models.DateTimeField(null=True, blank=True)
    display_email = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    ACCOUNT_REGISTRATION_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "password",
        "contact_number",
    ]

    _send_password_change_email = False
    add_this_password_to_history = None

    # pylint: disable=W0201
    def set_password(self, raw_password):
        super().set_password(raw_password)
        self.add_this_password_to_history = self.password

    # pylint: disable=C0415
    @cached_property
    def permission_codes(self):
        pass
        # from levelup.permission.models import LevelUpPermission
        #
        # groups = self.groups.all()
        # permissions = LevelUpPermission.objects.filter(groups__in=groups).values_list(
        #     "code", flat=True
        # )
        # return set(permissions)

    # pylint: disable=C0415
    @cached_property
    def humanized_permission_codes(self):
        pass
        # from levelup.permission.models import LevelUpPermission
        #
        # groups = self.groups.all()
        # permissions = LevelUpPermission.objects.filter(groups__in=groups).values_list(
        #     "humanized_var", flat=True
        # )
        # return set(permissions)

    @property
    def profile_picture_thumb(self):
        if self.profile_picture:
            return self.profile_picture.url

        from django.templatetags.static import static

        return static("user/images/default-pp.jpeg")

    @property
    def cover_image_thumb(self):
        if self.cover_image:
            return self.cover_image.url
        from django.templatetags.static import static

        return static("user/images/default_cover_picture.png")

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def display_name(self):
        return (
            f"{self.first_name} {self.last_name}".title()
            if not self.middle_name
            else f"{self.first_name} {self.middle_name} {self.last_name}".title()
        )

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        instance = super().save(*args, **kwargs)

        if hasattr(self, "add_this_password_to_history") and getattr(
            self, "add_this_password_to_history"
        ):
            self.password_history.create(password=self.add_this_password_to_history)
            if self._send_password_change_email:
                async_task(send_password_change_email, self.id)

        return instance


class PasswordChangeHistory(BaseModel):
    # user is required since , if password is changed by someone else , created_by gets his information rather than
    # the user for whom the password is being changed
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_history"
    )
    password = models.CharField("password", max_length=128)

    def __str__(self):
        return f"{self.created_at} | {self.user}"


class UserAccountSubscription(BaseModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class UserLoginMeta(TimeStampModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userloginmeta"
    )
    user_agent = models.TextField(null=True, blank=True)
    # max length for IPV6 is 39, including the colon (:) character
    ip_address = models.CharField(max_length=39, null=True, blank=True)
    private_ip = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Login meta for user => {self.user.email}"


class UserActivationToken(TimeStampModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_activation"
    )
    activation_token = models.CharField(editable=False, unique=True, max_length=32)


class CustomUserGroup(UUIDBaseModel):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, related_name="custom_user_group")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=get_custom_group_image_path, null=True, blank=True
    )

    def __str__(self):
        return self.name

    @property
    def image_thumb(self):
        if self.image:
            return self.image.url

        from django.templatetags.static import static

        return static("user/images/default.png")
