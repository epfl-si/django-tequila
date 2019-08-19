django-tequila
==============

`Tequila <http://tequila.epfl.ch/>`_ authentication for django.


Requirements
============

``django-tequila`` needs a modern version of Django – something after 1.10.
We aim to follow the last LTS, and we try as we can to follow the versions between LTS.

Latest known functioning version : 1.11.

This project also expects a fully operational `Tequila <http://tequila.epfl.ch/>`_ server.

Installation
============

    pip install django-tequila

Configuration
=============

You can find an django app example in `./django-tequila/sample_app`
Add a .env file like the .env.sample and the run it with Django 2 ::

    make build init-db


Or, for Django 1.11, prefix every make with the DOCKERFILES env set, like this ::

    DOCKERFILES='-f docker-compose-django1.yml' make build init-db

Then open `https://127.0.0.1/` in your browser

Use `make stop` to shut it down

settings.py
-----------

* Add at the end of your ``MIDDLEWARE_CLASSES``::

	'django_tequila.middleware.TequilaMiddleware',

* Add to ``INSTALLED_APPS``::

	'django_tequila',

* Add the line::

	AUTHENTICATION_BACKENDS = ('django_tequila.django_backend.TequilaBackend',)

* Set a name that will be displayed on the tequila login page::

	TEQUILA_SERVICE_NAME = "django_tequila_service"

* Finally, add / customize login/logout workflow ::

    LOGIN_URL = "/login"
    LOGIN_REDIRECT_URL = "/"
    LOGOUT_URL = '/'
    LOGIN_REDIRECT_IF_NOT_ALLOWED = "/not_allowed"
    LOGIN_REDIRECT_TEXT_IF_NOT_ALLOWED  = "Not allowed"

urls.py
-------

* Add these lines::

	from django_tequila.urls import urlpatterns as django_tequila_urlpatterns

	urlpatterns += django_tequila_urlpatterns


Profile customization
---------------------
You may want to keep some additional information about the user.
Take a look at `this page <http://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users>`_ for more information about profile customization.

Here is an example for a profile for Django 2.0

* Create a profile in your `models.py`, like this::

	from django.contrib.auth.models import AbstractUser
    from django.db import models


    class User(AbstractUser):
        # should map https://c4science.ch/diffusion/3359/browse/master/conf/LdapDataConnector.conf
        sciper = models.CharField(max_length=10, null=True, blank=True)
        where = models.CharField(max_length=200, null=True, blank=True)
        unit = models.CharField(max_length=200, null=True, blank=True)
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

* in your `settings.py`, tell django to use your model::

	AUTH_PROFILE_MODULE = "my_app.userprofile"

* Update your database::

	./manage.py syncdb

Site Admin customizations
-------------------------
If you want to use the admin site, be sure you have followed all steps to have a working django admin site,
then follow these steps :

* Modify your urls.py to look like this::

    from django.contrib import admin
    from django_tequila.admin import TequilaAdminSite
    admin.autodiscover()
    admin.site.__class__ = TequilaAdminSite

* Please note that your username should identical to the one you use to login in Tequila.
  If you do not have any user at the moment, or you want to edit some of them,
  create a superuser with this command (replace <USERNAME> and <EMAIL> with you Tequila username and email)::

    python manage.py createsuperuser --username=<USERNAME> --email=<EMAIL>


Additional tips and settings
============================

Advanced settings
-----------------

* If you need to use your personal server, change this parameter::

	TEQUILA_SERVER_URL = "https://tequila.epfl.ch"

* You may want to create an inactive user when someone try to connect to your app. So you can manually control who access it.
  If this is the case, add this line to `settings.py`::

	TEQUILA_NEW_USER_INACTIVE = True

* You may want to add some custom allow with Tequila.
  If this is the case, add this line to `settings.py`::

	TEQUILA_CONFIG_ALLOW = 'categorie=shibboleth'

  or, for multiple allow :

	TEQUILA_CONFIG_ALLOW = 'categorie=shibboleth|categorie=epfl-old'

* You may want to add some custom paramaters with Tequila.
  If this is the case, add this line to `settings.py`::

	TEQUILA_CONFIG_ADDITIONAL = {'allowedorgs': 'EPFL, UNIL'}

* Everytime the user connect trought the Tequila process, he is redirected to an url
  that has a 'key' paramter. For some esthetic reasons,you may want to remove this parameter,
  so add this line to `settings.py`::

    TEQUILA_CLEAN_URL = True

  As it creates a redirect to the cleaned address and add an additional page hit, The value by default is False

* You can force a strong authentication
  so add this line to `settings.py`::

    TEQUILA_STRONG_AUTHENTICATION = True

  Default value is False

* You may want to use a custom username value as for exemple the SCIPER.
  If this is the case, add this line to `settings.py`::

    TEQUILA_CUSTOM_USERNAME_ATTRIBUTE = 'uniqueid'

  Ex. : uniqueid, email, etc.

  Default value is username

    * You may want to allow multiple hosts to fetch requested information.
  If this is the case, add this line to `settings.py`::

    TEQUILA_ALLOWED_REQUEST_HOSTS = "the host ip"

  Ex. : "192.168.1.1|192.168.1.2"

  Default to None

Logging
-------

Sometimes we struggle to get the aimed result, showing some log may help :

* Add and customize as you need this logger to your settings ::

    'django_tequila': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },

Login/logout links
------------------

If you want the user to be redirected to a specific page after he logged/logout successfully, you have to add the 'next' parameter to your login url,
like the default Django authentication backend.
See `Django help for login-redirect-url <https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url>`_ for more information.


\(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
