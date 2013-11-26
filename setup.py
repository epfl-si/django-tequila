from distutils.core import setup

setup(
    name='django-tequila',
    version=__import__('django_tequila').__version__,
    
    author='Julien Delasoie',
    author_email='julien.delasoie at epfl ch',
    keywords='django, tequila, authentication',

    url='http://kis-doc.epfl.ch/django-tequila/',
    license="LGPLv3",
    description='A Tequila authentication backend for django',
    long_description=open('README', 'r').read(),

    packages = ['django_tequila',
                'django_tequila.django_backend',
                'django_tequila.tequila_client',
                'django_tequila.tequila_auth_views'],
    install_requires=('django>=1.6', ),
    
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