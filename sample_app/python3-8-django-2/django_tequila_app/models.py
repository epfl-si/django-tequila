"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2021
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'sciper'

    # fields here should map https://c4science.ch/diffusion/3359/browse/master/conf/LdapDataConnector.conf
    # see detail for epfl https://tequila.epfl.ch/cgi-bin/tequila/serverinfo
    sciper = models.CharField(max_length=10, unique=True, null=False, blank=False)
    where = models.CharField(max_length=200, null=True, blank=True)
    units = models.TextField(null=True, blank=True)
    classe = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, blank=True)
    group = models.TextField(null=True, blank=True)
    memberof = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return """  sciper:    %s
                        username:    %s
                        first_name: %s
                        last_name: %s
                        where:       %s
                        units:       %s
                        group:       %s
                        classe:      %s
                        statut:      %s
                        memberof:    %s
                    """ % (self.sciper,
                           self.username,
                           self.first_name,
                           self.last_name,
                           self.where,
                           self.units,
                           self.group,
                           self.classe,
                           self.statut,
                           self.memberof)
