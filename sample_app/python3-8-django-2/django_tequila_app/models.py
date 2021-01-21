"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'sciper'

    # should map https://c4science.ch/diffusion/3359/browse/master/conf/LdapDataConnector.conf
    sciper = models.CharField(max_length=10, null=True, blank=True, unique=True)
    where = models.CharField(max_length=200, null=True, blank=True)
    units = models.TextField(null=True, blank=True)
    classe = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, blank=True)
    group = models.TextField(null=True, blank=True)
    memberof = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return """  Sciper:    %s
                        where:     %s
                        units:     %s
                        group:     %s
                        classe:    %s
                        statut:    %s
                        memberof:  %s
                    """ % (self.sciper,
                           self.where,
                           self.units,
                           self.group,
                           self.classe,
                           self.statut,
                           self.memberof)
