# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['speedpycom']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.1.2,<5.0.0',
 'Pillow>=9.2.0,<10.0.0',
 'arrow>=1.2.3,<2.0.0',
 'boto3-stubs>=1.25.4,<2.0.0',
 'boto3>=1.25.4,<2.0.0',
 'celery-redbeat>=2.0.0,<3.0.0',
 'celery>=5.2.7,<6.0.0',
 'dj-database-url>=1.0.0,<2.0.0',
 'django-allauth>=0.51.0,<0.52.0',
 'django-braces>=1.15.0,<2.0.0',
 'django-cache-url>=3.4.2,<4.0.0',
 'django-ckeditor>=6.5.1,<7.0.0',
 'django-configurations>=2.4,<3.0',
 'django-cors-headers>=3.13.0,<4.0.0',
 'django-crispy-forms>=1.14.0,<2.0.0',
 'django-extensions>=3.2.1,<4.0.0',
 'django-import-export>=3.0.1,<4.0.0',
 'django-post-office>=3.6.3,<4.0.0',
 'django-redis>=5.2.0,<6.0.0',
 'django-ses>=3.2.1,<4.0.0',
 'django-storages>=1.13.1,<2.0.0',
 'django-tailwind>=3.4.0,<4.0.0',
 'django>=4.1.2,<5.0.0',
 'djangoql>=0.17.1,<0.18.0',
 'djangorestframework-simplejwt>=5.2.2,<6.0.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'drf-spectacular>=0.24.2,<0.25.0',
 'flower>=1.2.0,<2.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'honeybadger>=0.12.0,<0.13.0',
 'pillow>=9.2.0,<10.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'sentry-sdk>=1.10.1,<2.0.0',
 'wagtail>=4.0.4,<5.0.0',
 'wagtailcodeblock>=1.28.0,<2.0.0',
 'whitenoise>=6.2.0,<7.0.0']

setup_kwargs = {
    'name': 'speedpycom',
    'version': '0.1.16',
    'description': 'The Django Framework for SaaS',
    'long_description': '# SpeedPyCom – The Django Framework for SaaS\n\nBy [https://appliku.com/]()\n\n## Introduction\n\nSpeedPyCom is the collection of settings and requirements that allows you quick start of new production and deployment\nready Django Project for SaaS apps.\n\n## Some reasons you might want to use SpeedPyCom\n\n- Based on Django-Configurations, so while there is very useful base settings, it is easy to extend/override\n- Storages ready for S3 or local development\n- Credentials and some behaviour controlled via env vars\n- other useful apps and tools included\n\n## Discussions:\n\nJoin our Discord Community: https://appliku.com/discord\n\n',
    'author': 'Kostja P',
    'author_email': '123@appliku.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/speedpycom/speedpycom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
