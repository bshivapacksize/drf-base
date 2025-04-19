from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

USER = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        default model backend's authenticate method will return user 'None' if the user's is_active = False,
        to override this behavior and send proper response the custom backend is required
        """
        if username is None:
            username = kwargs.get(USER.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = USER._default_manager.get_by_natural_key(
                username
            )  # pylint: disable=W0212
        except USER.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            USER().set_password(password)
        else:
            if user.check_password(password):
                return user
