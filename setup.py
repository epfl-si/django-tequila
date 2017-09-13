"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from setuptools import setup

setup(
    name='django-tequila',
    version=__import__('django_tequila').__version__,
    
    author='Julien Delasoie',
    author_email='julien.delasoie@epfl.ch',
    keywords='django, tequila, authentication',

    url='https://github.com/epfl-idevelop/django-tequila',
    license="LGPLv3",
    description='A Tequila authentication backend for django',
    long_description=open('README.rst', 'r').read(),

    packages = ['django_tequila',
                'django_tequila.django_backend',
                'django_tequila.tequila_client',
                'django_tequila.tequila_auth_views'],

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ]
)