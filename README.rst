Platzigram
==========

Platzigram api is an api builded on Django REST Framework emulating the falso to be used as web service for multiple extra apss derivated to this project.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy platzigram_api

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



Base Local Enviroment Variables
-------------------------------

Django
^^^^^^
  USE_DOCKER=yes
  
  IPYTHONDIR=/app/.ipython

Postgres
^^^^^^^^
  POSTGRES_HOST

  POSTGRES_PORT

  POSTGRES_DB

  POSTGRES_USER

  POSTGRES_PASSWORD

Base Production Enviroment Variables
------------------------------------

Django
^^^^^^
  DJANGO_READ_DOT_ENV_FILE

  DJANGO_SETTINGS_MODULE

  DJANGO_SECRET_KEY

  DJANGO_ADMIN_URL

  DJANGO_ALLOWED_HOSTS

  DJANGO_SECURE_SSL_REDIRECT

  MAILGUN_API_KEY

  DJANGO_SERVER_EMAIL
  
  MAILGUN_DOMAIN

  DJANGO_AWS_ACCESS_KEY_ID

  DJANGO_AWS_SECRET_ACCESS_KEY

  DJANGO_AWS_STORAGE_BUCKET_NAME

  WEB_CONCURRENCY

  REDIS_URL

Postgres
^^^^^^^^
  POSTGRES_HOST

  POSTGRES_PORT

  POSTGRES_DB

  POSTGRES_USER

  POSTGRES_PASSWORD

