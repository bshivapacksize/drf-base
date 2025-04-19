from django.conf import settings

from rest_framework.permissions import BasePermission

from levelup.user.models import UserActivationToken


class LevelUpPermission(BasePermission):
    required_perm_codes = ["999999"]  # so that the permission always fails

    def has_permission(self, request, view):
        if not self.required_perm_codes:  # hack to block every request
            return False

        if not bool(request.user and request.user.is_authenticated):
            return False

        if isinstance(self.required_perm_codes, list):
            for code in self.required_perm_codes:
                if code not in request.user.permission_codes:
                    return False
            return True
        return False


def level_up_permission(required_perm_codes):
    return type(
        "PermissionForLevelUP",
        (LevelUpPermission,),
        dict(required_perm_codes=required_perm_codes),
    )


class MediaProcessPermission(BasePermission):
    def has_permission(self, request, view):
        perm_key = settings.CONTENT_PROCESS_CONFIRM_KEY
        authorization = request.headers.get("X-MEDIAAUTH")
        return perm_key == authorization


# class SystemAdminSuperMan(BasePermission):
#     def has_permission(self, request, view):
#         if bool(request.user and request.user.is_authenticated) and (
#             (request.user.id == 1 and request.user.is_superuser) or (
#                 request.user.email in ['shrwnkr@gmail.com', 'pshrawan@insightworkshop.io']
#         )):
#             return True
#         return False


class UserActivatePermission(BasePermission):
    def has_permission(self, request, view):
        activation_token = request.headers.get("X-ACTIVATION-TOKEN")
        activations = UserActivationToken.objects.filter(
            activation_token=activation_token
        )
        if activations:
            view.request.user = activations[0].user
            return True
        return False
