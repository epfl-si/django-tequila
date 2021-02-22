# -*- coding:utf-8 -*-

"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2021"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    def queryset(self, request):
        # prefetch the 'user' data to avoid N+1 SQL request
        return UserProfile.objects.all().select_related('user')

    def username(self, userprofile):
        return userprofile.user.username

    def email(self, userprofile):
        return userprofile.user.email

    def first_name(self, userprofile):
        return userprofile.user.first_name

    def last_name(self, userprofile):
        return userprofile.user.last_name

    def is_active(self, userprofile):
        return userprofile.user.is_active
    is_active.boolean = True

    def is_staff(self, userprofile):
        return userprofile.user.is_staff
    is_staff.boolean = True

    def is_superuser(self, userprofile):
        return userprofile.user.is_superuser
    is_superuser.boolean = True

    list_display = UserAdmin.list_display + ('is_active', 'is_superuser', )
    search_fields = list(['user__' + f for f in UserAdmin.search_fields])
    fieldsets = (
        (None, {'fields': ('user',)}),
        ("Tequila", {'fields': ('sciper', 'where', 'units', 'memberof',
                                'group', 'classe', 'statut')})
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(verbose_name="", is_stacked=False)},
    }


admin.site.register(UserProfile, UserProfileAdmin)
