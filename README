==========================================================
`django-tequila <http://kis-doc.epfl.ch/django-tequila/>`_
==========================================================

`Tequila <http://tequila.epfl.ch/>`_ authentication for django.


Requirements
============

``django-tequila`` needs a modern version of Django – something after 1.1.
This project also expects a fully operational `Tequila <http://tequila.epfl.ch/>`_ server.

Installation
============

    pip install django-tequila
	
Configuration
=============

You can find an django app example in ``./django-tequila/sample_app``

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
	
* Finally, add::

	LOGIN_URL = "/login"
	LOGIN_REDIRECT_URL = "/"
	LOGIN_REDIRECT_IF_NOT_ALLOWED = "/not_allowed"
        LOGOUT_URL = '/'

urls.py
-------

* Add these lines::
	
	from django_tequila.urls import urlpatterns as django_tequila_urlpatterns
	
	urlpatterns += django_tequila_urlpatterns


Profile customization
---------------------
You may want to keep some additional informations about the user.
Take a look at `this page <http://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users>`_ for more informations about profile customization.

* Create a profile in your `models.py`, like this::

	from django.contrib.auth.models import User
	from django.db import models
	
	class UserProfile(models.Model):
	    #required field
	    user = models.ForeignKey(User, unique=True)
	    
	    sciper = models.PositiveIntegerField(null=True, blank=True)
	    where = models.CharField(max_length=100, null=True, blank=True)
	    units = models.CharField(max_length=300, null=True, blank=True)
	    group = models.CharField(max_length=150, null=True, blank=True)
	    classe = models.CharField(max_length=100, null=True, blank=True)
	    statut = models.CharField(max_length=100, null=True, blank=True)
	    
	# Trigger for creating a profile on user creation 
	def user_post_save(sender, instance, **kwargs):
	    profile, new = UserProfile.objects.get_or_create(user=instance)
	
	# Register the trigger
	models.signals.post_save.connect(user_post_save, sender=User)

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

* You may want to create an inactive user when someone try to connect to your app. So you can manually control who access it. 
  If this is the case, add this line to `settings.py`::

	TEQUILA_NEW_USER_INACTIVE = True
	
* You may want to add some custom allow with Tequila. 
  If this is the case, add this line to `settings.py`::

	TEQUILA_CONFIG_ALLOW = 'categorie=shibboleth'
	
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

Login/logout links
------------------

If you want the user to be redirected to a specific page after he logged/logout successfully, you have to add the 'next' parameter to your login url,
like the default Django authentication backend.
See `Django help for login-redirect-url <https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url>`_ for more informations.


Help & Contributing
===================
Feel free to contact me (julien dot delasoie at epfl dot ch) with any questions or concerns you may have with the
module.

Source code
-----------
The EPFL Sphinx theme is hosted on the `EPFL git repository <http://git.epfl.ch>`_, at https://git.epfl.ch/repo/django-tequila.git.

