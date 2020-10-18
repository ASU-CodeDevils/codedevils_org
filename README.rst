codedevils.org
==============

The official CodeDevils website. Check out our `Documentation`_ for more information.

.. _`Documentation`: https://asu-codedevils.github.io/codedevils_org/

.. image:: https://travis-ci.com/ASU-CodeDevils/codedevils.org.svg?branch=master
    :target: https://travis-ci.com/ASU-CodeDevils/codedevils.org
    :alt: Build
.. image:: https://codecov.io/gh/ASU-CodeDevils/codedevils.org/branch/master/graph/badge.svg?token=FF94MF9N4M
    :target: https://codecov.io/gh/ASU-CodeDevils/codedevils.org
    :alt: Codecov
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/pydanny/cookiecutter-django/
    :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Black code style
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/badge/chat-slack-pink.svg
    :target: https://codedevils.slack.com/archives/GPNBSDM27
    :alt: Slack

Website Status
--------------

Production
^^^^^^^^^^

.. image:: https://travis-ci.com/ASU-CodeDevils/codedevils.org.svg?branch=master
    :target: https://travis-ci.com/ASU-CodeDevils/codedevils.org
    :alt: Build
.. image:: https://img.shields.io/uptimerobot/status/m784417521-1b9dcabb76b05ae6fdc099b3
    :target: https://codedevils.org
    :alt: Status (prod)
.. image:: https://img.shields.io/uptimerobot/ratio/m784417521-1b9dcabb76b05ae6fdc099b3
    :target: https://status.codedevils.org/784417521
    :alt: Uptime (prod)

QA
^^

.. image:: https://travis-ci.com/ASU-CodeDevils/codedevils.org.svg?branch=dev
    :target: https://travis-ci.com/ASU-CodeDevils/codedevils.org
    :alt: Build
.. image:: https://img.shields.io/uptimerobot/status/m784417527-57e543ec1e2e0752a9ba2228
    :target: https://qa.codedevils.org
    :alt: Status (QA)
.. image:: https://img.shields.io/uptimerobot/ratio/m784417527-57e543ec1e2e0752a9ba2228
    :target: https://status.codedevils.org/784417527
    :alt: Uptime (QA)

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy codedevils_org

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



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd codedevils_org
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


Sphinx Documentation
^^^^^^^^^^^^^^^^^^^^
To build the documentation for GitHub pages, run the following:

.. code-block:: bash

    cd sphinx
    make github

This will generate the documentation in the `docs` directory which will automatically update GitHub pages
when the `master` branch is updated.

Deployment
----------

Deployment instructions are not available publicly.
