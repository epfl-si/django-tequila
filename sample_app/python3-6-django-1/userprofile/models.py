"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """ UserProfile model """
    user = models.OneToOneField(User, null=True, related_name="profile", on_delete=models.CASCADE)

    sciper = models.CharField(max_length=10, null=True, blank=True)
    where = models.CharField(max_length=200, null=True, blank=True)
    units = models.TextField(null=True, blank=True)
    group = models.TextField(null=True, blank=True)
    classe = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, blank=True)
    memberof = models.TextField(null=True, blank=True)

    def __unicode__(self):
        full_name = u'%s %s' % (self.user.last_name, self.user.first_name)
        return full_name.strip() or self.user.username


# Trigger for creating a profile on user creation
def user_post_save(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)

# Register the trigger
models.signals.post_save.connect(user_post_save, sender=User)

