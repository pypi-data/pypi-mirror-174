================
Cookiecutter C++
================

.. image:: https://circleci.com/gh/grhawk/cookiecutter-cpp.svg?style=shield
    :target: https://circleci.com/gh/grhawk/cookiecutter-cpp
    :alt: Build Status

Cookiecutter_ template for a C++ package.

* GitHub repo: https://github.com/grhawk/cookiecutter-cpp/
* Documentation (this is for cookiecutter-pypackage): https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license


Credits
-------
This is basically a fork of Cookiecutter_.


Features
--------

* Testing setup with ``gtest``
* Circleci_: Ready for Circleci Continuous Integration testing
* Doxigen_ docs: TODO!
* bump2version_: TODO!
* Command line interface using CLI11 (optional)
* Logging system using spdlog

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter

Build Status
-------------

Linux:

.. image:: https://circleci.com/gh/grhawk/cookiecutter-cpp.svg?style=shield
    :target: https://circleci.com/gh/grhawk/cookiecutter-cpp
    :alt: Linux build status on Travis CI

Windows:
TODO!


Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/grhawk/cookiecutter-cpp.git

Then:

* Create a repo and put it there.
* Add the repo to your Circleci_ account.

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html

Not Exactly What You Want?
--------------------------

Don't worry, you have options:

Fork This / Create Your Own
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

* Once you have your own version working, add it to the Similar Cookiecutter
  Templates list above with a brief description.

* It's up to you whether or not to rename your fork/own version. Do whatever
  you think sounds good.

Or Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.


.. _Circleci: http://circleci.com/
.. _Tox: http://testrun.org/tox/
.. _Doxigen: http://doxigen.org/
.. _Read the Docs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _bump2version: https://github.com/c4urself/bump2version
.. _Punch: https://github.com/lgiordani/punch
.. _Poetry: https://python-poetry.org/
.. _PyPi: https://pypi.python.org/pypi
.. _Mkdocs: https://pypi.org/project/mkdocs/

.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`tony/cookiecutter-pypackage-pythonic`: https://github.com/tony/cookiecutter-pypackage-pythonic
.. _`ardydedase/cookiecutter-pypackage`: https://github.com/ardydedase/cookiecutter-pypackage
.. _`lgiordani/cookiecutter-pypackage`: https://github.com/lgiordani/cookiecutter-pypackage
.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage
.. _`veit/cookiecutter-namespace-template`: https://github.com/veit/cookiecutter-namespace-template
.. _`zillionare/cookiecutter-pypackage`: https://zillionare.github.io/cookiecutter-pypackage/
.. _github comparison view: https://github.com/tony/cookiecutter-pypackage-pythonic/compare/audreyr:master...master
.. _`network`: https://github.com/audreyr/cookiecutter-pypackage/network
.. _`family tree`: https://github.com/audreyr/cookiecutter-pypackage/network/members
