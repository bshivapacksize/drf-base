import random

import string

from django.contrib.auth import get_user_model

from django.core.mail import send_mail

from django.conf import settings

from django.template.loader import render_to_string

# from levelup.permission.constants import CAN_CREATE_PROFILES_OF_ROLES
#
# from levelup.user.constants import VALID_PROFILE_COMPLETE_FIELD_CHOICES


def send_html_template_email(
    subject, message_text, from_email, receiving_emails, html_template, context
):
    html_message = render_to_string(html_template, context=context)

    send_mail(
        subject, message_text, from_email, receiving_emails, html_message=html_message
    )


def send_password_change_email(user_id):
    from django.contrib.auth import get_user_model

    USER = get_user_model()

    user = USER.objects.get(id=user_id)

    context = {
        "full_name": user.first_name,
    }

    txt_message_template = "user/password_change.txt"

    html_message_template = "user/password_change.html"

    message = render_to_string(txt_message_template, context=context)

    html_message = render_to_string(html_message_template, context=context)

    send_mail(
        "LevelUp - Your Password has been changed",  # make prefix dynamic
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )


def send_on_board_email(user_id, context):
    user = get_user_model().objects.get(id=user_id)

    txt_message_template = "user/account_activation.txt"

    html_message_template = "user/account_activation.html"

    message = render_to_string(txt_message_template, context=context)

    html_message = render_to_string(html_message_template, context=context)

    send_mail(
        "LevelUp - Account Activation",  # make prefix dynamic
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )


def send_free_course_on_board_email(user_id, context):
    user = get_user_model().objects.get(id=user_id)

    txt_message_template = "user/account_activation.txt"

    html_message_template = "user/free_course.html"

    message = render_to_string(txt_message_template, context=context)

    html_message = render_to_string(html_message_template, context=context)

    send_mail(
        "LevelUp - Account Activation",  # make prefix dynamic
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )


def random_password():
    letters = string.ascii_letters + string.digits

    return "".join(random.choice(letters) for _ in range(10))


def send_email_for_admin_created_user(first_name, email, password):
    message = """Dear {},

Welcome to Levelup

Your LevelUp login credentials

Email: {}

Password: {}

Changing password after first login is always a good practice.


Do not reply this email.

If you have any problem, contact support at support@leveluptech.io


LevelUp Team

""".format(
        first_name, email, password
    )

    send_mail(
        "LevelUp Account Credentials", message, settings.DEFAULT_FROM_EMAIL, [email]
    )


def user_need_profile_complete_check(user):
    if CAN_CREATE_PROFILES_OF_ROLES in user.permission_codes:
        return True

    return False


def get_profile_required_fields(user):
    user_profile_complete_required = user_need_profile_complete_check(user)

    if user_profile_complete_required:
        return VALID_PROFILE_COMPLETE_FIELD_CHOICES

    return []


def is_user_profile_completed(user):
    has_profile_picture = True if user.profile_picture else False

    has_cover_image = True if user.cover_image else False

    required_fields = get_profile_required_fields(user)

    if not has_cover_image:
        return False

    if not has_profile_picture:
        return False

    profile = getattr(user, "user_profile", None)

    if not profile:
        return False

    for required_field in required_fields:

        if not getattr(profile, required_field, None):
            return False

    return True
