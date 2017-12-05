# Changelog
All notable changes to this project will be documented in this file.


## [Todo]


## [Unreleased]
### Added
- Allow to get a different attribute for username value

### Changed
- Use get_user_model to get the User (thanks llann)
- Remove LICENSE file, as 2.1.8 added copyright in source. The license should be more permissive now.

### Fixed
- Some PEP8 formatting for *.py files
- Django 1.11.x and python 3 compatibilities

### Changed
- Use get_user_model to get the User (thanks llann)
- Remove LICENSE file, as 2.1.8 added copyright in source. The license should be more permissive now.

### Fixed
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
