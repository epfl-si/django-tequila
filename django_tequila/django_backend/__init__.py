"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""
import logging

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth import get_user_model
from django_tequila.tequila_client import TequilaClient
from django_tequila.tequila_client.config import EPFLConfig
from django.conf import settings
from django.db.utils import OperationalError

logger = logging.getLogger('django_tequila.backend')
User = get_user_model()


class TequilaBackend(RemoteUserBackend):
    """
    Authenticate against a Tequila server, using the TequilaClient class
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """
    create_unknown_user = True

    """ Created user should be inactive by default ?"""
    try:
        set_created_user_at_inactive = settings.TEQUILA_NEW_USER_INACTIVE
    except AttributeError:
        set_created_user_at_inactive = False

    """ Set server url"""
    try:
        tequila_server_url = settings.TEQUILA_SERVER_URL
    except AttributeError:
        tequila_server_url = ""

    def authenticate(self, request, token=None):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """

        tequila_key = token

        if not tequila_key:
            return
        user = None

        try:
            allowedrequesthosts = settings.TEQUILA_ALLOWED_REQUEST_HOSTS
        except AttributeError:
            allowedrequesthosts = None

        if self.tequila_server_url:
            user_attributes = TequilaClient(
                EPFLConfig(server_url=self.tequila_server_url)).get_attributes(
                tequila_key, allowedrequesthosts)
        else:
            user_attributes = TequilaClient(EPFLConfig()).get_attributes(
                tequila_key, allowedrequesthosts)

        # Give de possibility to choose a cusom value for the local username field
        custom_username_field = getattr(settings,
                                        'TEQUILA_CUSTOM_USERNAME_ATTRIBUTE',
                                        'username')
        username = user_attributes[custom_username_field]

        # keep only the first username, not the user@unit or the multiple users
        if username.find(","):
            username = username.split(",")[0]
            if username.find("@"):
                username = username.split("@")[0]

        # Note that this could be accomplished in one try-except clause,
        # but instead we use get_or_create when creating unknown users since
        # it has built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = User.objects.get_or_create(**{
                User.USERNAME_FIELD: username
            })
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = User.objects.get(**{
                    User.USERNAME_FIELD: username
                })
            except User.DoesNotExist:
                pass

        if user:
            # updates data in all cases
            self.update_attributes_from_tequila(user, user_attributes)

            if self.user_can_authenticate(user):
                # all good !
                return user

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)

        return is_active or is_active is None

    @staticmethod
    def _try_to_set_user_attributes(user, mapping, user_attributes):
        """ As applications may have a different model without the needed fields,
            be kind with forgiveness
            mapping is the attribute_name in Django, user_attributes in Tequila
            ex: (('sciper','uniqueid'), ...)
        """
        # for django >1.9 compatibilities
        if hasattr(user, "profile"):
            attributes_model = user.profile
        else:
            attributes_model = user

        for model_field, tequila_field in mapping:
            try:
                if user_attributes.get(tequila_field):
                    setattr(attributes_model, model_field, user_attributes.get(tequila_field))
            except (AttributeError, OperationalError):
                logger.warning(
                    'Unable to save the Tequila attribute {} in user.{}'
                    ' Does the User model can handle it ?'.format(tequila_field, model_field))

        # for django >1.9 compatibilities
        if hasattr(user, "profile"):
            user.profile.save()

    def update_attributes_from_tequila(self, user, user_attributes):
        """ Fill the user profile with tequila attributes """
        mapping = (
            ('sciper', 'uniqueid'),
            ('where', 'where'),
            ('units', 'allunits'),
            ('group', 'group'),
            ('classe', 'classe'),
            ('statut', 'statut'),
            ('memberof', 'memberof'),
        )

        self._try_to_set_user_attributes(user, mapping, user_attributes)

        # check for create or update field part
        if user_attributes['firstname']:
            first_name_attribute = user_attributes['firstname']
            # try a manual truncate if necessary,
            # else allow the truncate warning to be raised
            if len(first_name_attribute) > \
                    user._meta.get_field('last_name').max_length \
                    and first_name_attribute.find(',') != -1:
                first_name_formatted = first_name_attribute.split(',')[0]
            else:
                first_name_formatted = first_name_attribute

            if user.first_name:
                # need update ?
                if user.first_name != first_name_formatted:
                    user.first_name = first_name_formatted
            else:
                user.first_name = first_name_formatted
        if user_attributes['name']:
            if user.last_name:
                if user.last_name != user_attributes['name']:
                    user.last_name = user_attributes['name']
            else:
                user.last_name = user_attributes['name']

        if user_attributes['email']:
            if user.email:
                if user.email != user_attributes['email']:
                    user.email = user_attributes['email']
            else:
                user.email = user_attributes['email']

        user.save()

    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        if self.set_created_user_at_inactive:
            user.is_active = False
            user.save()
        return user
