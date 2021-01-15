"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

ADDITIONAL_USER_FIELDS = (('Tequila fields', {'fields': ('sciper',
                                                         'where',
                                                         'units',
                                                         'group',
                                                         'classe',
                                                         'statut',
                                                         'memberof',
                                                         )}),)


class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS


admin.site.register(User, MyUserAdmin)
