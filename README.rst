django-tequila
==============

`Tequila <http://tequila.epfl.ch/>`_ authentication for django.


Requirements
============

``django-tequila`` needs the Django 2.2 LTS

This project also expects a fully operational `Tequila <http://tequila.epfl.ch/>`_ server.

Installation
============

    pip install django-tequila

Configuration
=============

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

Login/logout links
------------------

If you want the user to be redirected to a specific page after he logged/logout successfully, you have to add the 'next' parameter to your login url,
like the default Django authentication backend.
See `Django help for login-redirect-url <https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url>`_ for more information.


Profile customization
---------------------
You may want to keep some additional information about the user.
Take a look at `this page <http://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users>`_ for more information about profile customization.

Here is an example for a profile for Django 2.0

* Create a custom User model in your `models.py` (see ./sample_app/python3-8-django-2/django_tequila_app/models.py)

* in your `settings.py`, tell django to use your model (see ./sample_app/python3-8-django-2/django_tequila_app/settings.py)::
    AUTH_USER_MODEL = 'my_app.User'
    TEQUILA_CUSTOM_USERNAME_ATTRIBUTE = "uniqueid"


* Update your database::

	./manage.py syncdb

Site Admin customizations
-------------------------

- Add or modify your admin.py file, like ./sample_app/python3-8-django-2/django_tequila_app/admin.py


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
  that has a 'key' parameter. For some esthetic reasons,you may want to remove this parameter,
  so add this line to `settings.py`::

    TEQUILA_CLEAN_URL = True

  As it creates a redirect to the cleaned address and add an additional page hit, The value by default is False

* You can force a strong authentication
  so add this line to `settings.py`::

    TEQUILA_STRONG_AUTHENTICATION = True

  Default value is False

* The only value that is truly unique is the sciper ('uniqueid' in Tequila). If your application
  need a different usage, you can set to a different field (at your own risk though). You can add this line to `settings.py`::

    TEQUILA_CUSTOM_USERNAME_ATTRIBUTE = 'uniqueid'

  Ex. : username, email, etc.

  Default value is username

* You may want to allow multiple hosts to fetch requested information.
  If this is the case, add this line to `settings.py`::

    TEQUILA_ALLOWED_REQUEST_HOSTS = "the host ip"

  Ex. : "192.168.1.1|192.168.1.2"

  Default to None

* You can allow guests to log in
  so add this line to `settings.py`::

    TEQUILA_ALLOW_GUESTS = True

  Default value is False


Sample app
===========

You can find some django app examples in `./django-tequila/sample_app/python3-8-django-2`
Add a .env file like the  `./.env.sample` and the run it with Django 2, at the root of the project ::

    make build init-db


Or, for Django 1.11, prefix every make with the DOCKERFILES env set, like this ::

    DOCKERFILES='-f sample_app/python3-6-django-1/docker-compose.yml' make build init-db

Then open `https://127.0.0.1/` in your browser

Use `make stop` to shut it down

Logging
-------

Sometimes we struggle to get the aimed result, showing some log may help :

* Add and customize as you need this logger to your settings ::

    'django_tequila': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },

Debugging
---------

* The sample app can be used to debug. We use remote_pdb for this case. Set this snippet in the code ::

    from remote_pdb import RemotePdb
    RemotePdb('127.0.0.1', 4445).set_trace()

* Then go into the container ::

    make bash

* Finally connect to the debug session with ::

    telnet 127.0.0.1 4445


\(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI
