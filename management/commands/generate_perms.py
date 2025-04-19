from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

from django.core.management.base import BaseCommand

from commons.constants import ADMIN, CREATOR, REVIEWER, USER

from commons.constants import (
    ADMIN_WANTS,
    CONTENT_ADMIN_WANTS,
    NORMAL_USER_WANTS,
    PERMISSIONS,
    REVIEWER_WANTS,
)

from ...models import LevelUpPermission


class Command(BaseCommand):

    def handle(self, *args, **options):

        admin, _ = Group.objects.get_or_create(name=ADMIN)

        content_admin, _ = Group.objects.get_or_create(name=CREATOR)

        reviewer, _ = Group.objects.get_or_create(name=REVIEWER)

        normal_user, _ = Group.objects.get_or_create(name=USER)

        for permission in PERMISSIONS:

            obj, _ = LevelUpPermission.objects.update_or_create(
                code=permission["code"], defaults=permission
            )

            if permission["code"] in ADMIN_WANTS:

                admin.levelup_permissions.add(obj)

            elif permission["code"] in CONTENT_ADMIN_WANTS:

                content_admin.levelup_permissions.add(obj)

            elif permission["code"] in REVIEWER_WANTS:

                reviewer.levelup_permissions.add(obj)

            elif permission["code"] in NORMAL_USER_WANTS:

                normal_user.levelup_permissions.add(obj)

        try:

            user = get_user_model().objects.filter(id=1, is_superuser=True).get()

        except get_user_model().DoesNotExist:

            user = None

        else:

            user.groups.add(admin)
