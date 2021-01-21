"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2021
"""
import logging

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth import get_user_model
from django_tequila.tequila_client import TequilaClient
from django_tequila.tequila_client.config import EPFLConfig
from django.conf import settings
from django.db.utils import OperationalError
from django.apps import apps

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

        # TODO: add username field in example, as User.profile and as seperated field in User
        # TODO: set sciper field as unique=True

        # username has a tricky format, fix it
        if user_attributes.get('username'):
            u_name = user_attributes['username']
            if u_name.find(","):
                u_name = u_name.split(",")[0]
                if u_name.find("@"):
                    u_name = u_name.split("@")[0]
                user_attributes['username'] = u_name

        # Note that this could be accomplished in one try-except clause,
        # but instead we use get_or_create when creating unknown users since
        # it has built-in safeguards for multiple threads.
        if self.create_unknown_user:
            # fetching a unique user, it should be the user.profile.sciper if available
            user, created = self.get_user_from_db(user_attributes, create=True)
            if created:
                user = self.configure_user(user)
        else:

            user, created = self.get_user_from_db(user_attributes, create=False)

        if user:
            # updates data in all cases
            self.update_attributes_from_tequila(user, user_attributes)

            if self.user_can_authenticate(user):
                # all good !
                return user

    def get_user_from_db(self, user_attributes, create=True):
        """
        :return: Returns a tuple of (object, created),
        where object is the retrieved or created object and
        created is a boolean specifying whether a new object was created.
        """
        user = None

        # find the sciper first, as it is the only unique value from Tequila
        tequila_sciper = user_attributes.get('uniqueid')
        tequila_username = user_attributes.get('username')

        # current app is using a user profile ?
        is_app_using_profile = hasattr(settings, 'AUTH_PROFILE_MODULE')

        if is_app_using_profile:
            user_profile_model = apps.get_model(*settings.AUTH_PROFILE_MODULE.split('.'))

            try:
                user_profile = user_profile_model.objects.filter(sciper=tequila_sciper).latest('id')
                user = user_profile.user
            except user_profile_model.DoesNotExist:
                pass
            except User.DoesNotExist:
                # recreate missing user and connect to his orphan profile
                self.backup_user_with_same_username(tequila_username)
                user = User.objects.create(username=tequila_username, id=user_profile.user_id)
                return user, True
        else:
            # No profile, so think it as an AbstractUser with USERNAME_FIELD
            # Give de possibility to choose a custom value for the local username field
            custom_username_field = getattr(settings,
                                            'TEQUILA_CUSTOM_USERNAME_ATTRIBUTE',
                                            'username')  # should be uniqueid if we do it right
            #TODO: raise obsolete warning if TEQUILA_CUSTOM_USERNAME_ATTRIBUTE='username' is used here
            tequila_user_identifier = user_attributes[custom_username_field]

            try:
               user = User.objects.get(**{
                   User.USERNAME_FIELD: tequila_user_identifier
               })
            except User.DoesNotExist:
               pass

        if user:
            # update the User.username, in case it has changed
            if user.username != tequila_username:
                self.backup_user_with_same_username(tequila_username)
                user.username = tequila_username
                user.save()

            return user, False

        elif create:  # create a new user
            self.backup_user_with_same_username(tequila_username)
            user = User.objects.create(username=tequila_username)
            return user, True

        else:
            return user, False

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)

        return is_active or is_active is None

    def backup_user_with_same_username(self, username):
        """
        As username may be already taken,
        free it before giving to the connecting user
        """
        try:
            # other_user is an another user with same username
            other_user = User.objects.get(username=username)
            other_user.username = other_user.username + '-inactive-' + str(other_user.id)
            other_user.save()
        except User.DoesNotExist:
            pass

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
