import os
from django.contrib.auth import get_user_model
from django.conf import settings

sciper = os.environ.get('SUPER_ADMIN_SCIPER')
email = os.environ.get('SUPER_ADMIN_EMAIL')
username = os.environ.get('SUPER_ADMIN_USERNAME')
password = os.environ.get('SUPER_ADMIN_PASSWORD')

User = get_user_model()
User.objects.filter(email=email).delete()
u = User.objects.create_superuser(username=username, email=email, password=None, sciper=sciper)

is_app_using_profile = hasattr(settings, 'AUTH_PROFILE_MODULE')

if is_app_using_profile:
    u.profile.sciper = sciper
    u.profile.save()
else:
    u.sciper = sciper
    u.save()
