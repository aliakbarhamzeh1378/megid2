from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api.base.managers import userModelManager
from api.base.v1.models.permisionsModel import PermissionModel


class UserModel(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    Email = models.EmailField(_('email address'), null=False, unique=True)
    Username = models.CharField(max_length=100, null=False, unique=True)
    Permissions = models.ForeignKey(PermissionModel, on_delete=models.DO_NOTHING, null=True, blank=True)
    Slave_id = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = ['Email']

    objects = userModelManager()

    def __str__(self):
        return self.Email
