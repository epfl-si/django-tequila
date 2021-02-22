# Changelog
All notable changes to this project will be documented in this file.

## 3.3.0
### Change
- the Remedy version : due to a change how Tequila manage the users identification, this version is a transition to a unique config, with the Django Username being the field "sciper".
    - In detail, if a person is not active anymore inside Tequila, as Tequila username or email field can be redistributed to a new person, the only real unique ID for a person is the sciper ('uniqueid' in Tequila)

- If you used so something else into TEQUILA_CUSTOM_USERNAME_ATTRIBUTE as uniqueid, a special behavior (see next point) is put in place to keep every user unique. You are not forced to change anything, though you can have overlapping users if you keep away from the 'uniqueid' field.
  
- To mitigate this change, this version use a special behavior : when a user is found with the same sciper but with an already existing username field : we rename (see `def backup_user_with_same_username` in django_tequila/django_backend/__init__.py) the "old" username to keep every user different. Of course, to identify this user, a sciper field should be set into the User model. 

- Please consider verifying and, if needed, changing your models, your data and your settings. 

- For the version 3.3.0 (not mandatory but highly recommanded) :
    - Assert your model has a sciper field and is not empty, so user can be identify has unique :
        - class User(AbstractUser): ...  sciper = models.CharField(max_length=10, null=True, blank=True, unique=True) ...

- For the next major version :
    - Assert your settings use the only field wanted in Tequila :
        - TEQUILA_CUSTOM_USERNAME_ATTRIBUTE = "uniqueid"
  - Assert your model use it as primary field
      - class User(AbstractUser): ... USERNAME_FIELD = 'sciper'

- see ./sample_app/python3-8-django-2 for a good app sample

## 3.2.0
### Change
- Update to Django 2.2

### Fix
- Being able to redirect to a different site after logout

## 3.1.0
### Added
- Allow guests settings

## 3.0.2
### Fix
- Version number in .py

## 3.0.1
### Added
- Tools for debugging the sample_app

### Fix
- Fix missing save on user's profile

## 3.0.0
### Added
- A test framework trough docker
- Add allowedrequesthosts parameter

### Change
- Compatible with Django 2.1. Meaning we will suport only django 1.11 and 2.1
- Update the sample_app to reflect this evolution

### Fix
- Sample_app work with SSL
- Fix field mapping for user, as some field where too small. Be warned, you may need to migrate your DB to reflect the change (see https://github.com/epfl-idevelop/django-tequila/commit/1f2f8af0bcd81c6dbd8d9a2385fbc17174f34ba3).
- Fix pip installation encoding failure

## 2.1.18
### Fix
- Django authentication backend may not return any user
- Security fix : Force redirect url to have a slash

## 2.1.17
### Fix
- Bump version for Pypi

## 2.1.16
### Added
- Allow to get a different attribute for username value

### Changed
- Use get_user_model to get the User (thanks llann)
- Remove LICENSE file, as 2.1.8 added copyright in source. The license should be more permissive now.
- Removing the 2.1.10 change that allow the force https redirect, as Tequila will do it by default.

### Fixed
- Security fix : Disallow a redirect to a different site than the origin
- Django 1.11.x and python 3 compatibilities
- Some PEP8 formatting for *.py files

## 2.1.15
### Fixed
- Check if user.is\_active==True before allowing user to connect

## 2.1.14
### Fixed
- Accidently removing other parameters in url than the ask one, like 'key'

## 2.1.13
### Changed
- a user profile is optional

## 2.1.12
### Changed
- Force UTF-8 on Tequila reply string

## 2.1.11
### Fixed
- Force https after Tequila authentification

## 2.1.10
### Added
- Add an option to force https if redirect url is not or half provided

### Changed
- Force https for EPFL configuration

## 2.1.9
### Changed
- Move to Django 1.11
- Update links to doc
- Print more detail for current user in sample_app

## 2.1.8
### Added
- Copyright informations in source

## 2.1.7
### Added
- Better logs for the Tequila Client lib

### Fixed
- Some tequila return were not parsed

## 2.1.6
### Removed
- Remove unused import of RequestSite

## 2.1.5
### Changed
- Moved to Django 1.10

## 2.1.4
### Fixed
- Wrong import for Python 3
- Admin url

## 2.1.3
### Changed
- Moved to Django 1.9

## 2.1.2
### Added
- Added some documentation on multiple configuration

## 2.1.1
### Fixed
- Redirect to a HTTPS URL

## 2.1.0
### Added
- Python 3 compatibilities

## 2.0.4
### Changed
- Django is no more required, only recommended

## 2.0.3
### Changed
- Moved to Django 1.8

## 2.0.2
### Fixed
- Fix for the new Tequila username model

## 2.0.1
### Changed
- Apply any changes found from Tequila to the local model

## 2.0.0
### Changed
- Moved to Django 1.6

## 1.9.6
### Fixed
- Doc

## 1.9.5
### Fixed
- TEQUILA_CLEAN_URL work with Django 1.5+ now

## 1.9.4
### Added
- Allow to set server_url from settings

## 1.9.3
### Fixed
- Versionning

## 1.9.2
### Fixed
- Missing server_url parameter

## 1.9.1
### Changed
- Switched repository to git
- improved distribution

### Fixed
- typos in documentation

## 1.9
### Added
- Strong authentication option

## 1.8
### Changed
Users have a sciper that is a string now, switching from int to string in the profile model for the sciper.

## 1.7
### Added
- Admin view for profile

### Fixed
- Fixed too long first-name if truncate is possible

## 1.6
### Changed
* Moved to Django 1.4

## 1.5
### Added
- Added an optional way to remove the disgracious 'key' parameter from url

### Changed
- Allowed redirection after a logout

## 1.4
### Added
- Admin Site configuration and examples

## 1.3
### Added
- TEQUILA_CONFIG_ALLOW option to set a custom allow parameter
- TEQUILA_CONFIG_ADDITIONAL option to set a custom parameter

## 1.2
### Added
- "memberof" attribute

### Changed
- Tequila python client doesn't need django anymore
- Warning :	You have to change your settings to "AUTHENTICATION_BACKENDS = ('django_tequila.django_backend.TequilaBackend',)" if you used the 1.1 version

## 1.1
### Changed
- Better url separation
- Separated sample and functionality
- Easier installation by using pip or python setup.py install
- Renamed from tequila-django to django-tequila

## 1.0
### Added
- Initial release
