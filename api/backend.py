from django.conf import settings
from django.contrib.auth.backends import BaseBackend, UserModel


class SettingsBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):

        username_kwargs = {'Username': username}
        email_kwargs = {'Email': username}
        try:
            user = UserModel.objects.get(**username_kwargs)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(**email_kwargs)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
