from django.contrib.auth.models import Group
from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField(Group, related_name="levelup_permissions")
    code = models.CharField(unique=True, max_length=5)
    description = models.TextField(blank=True)
    humanized_var = models.CharField(max_length=255)

    def __str__(self):
        return self.name
