===========
Class Cloud
===========

About
=====

Class Cloud is a course management software application designed for ease of use
and ubiquity across all modern web capable devices
i.e. Desktop Browsers, Tablets, and Phones.

The Setup before you start coding
=================================

1. Install virtualenv
    In debian this is done via::

        sudo apt-get install python-virtualenv

2. Clone this repository
3. cd into the Class-Cloud folder
4. create a virtualenvironment
    In debian this is done via::

        virtualenv ENV

5. type the following inthe commandline::

    source ENV/bin/activate

6. you should not install django via pip::

    pip install django
    
Other things installed
======================

.. code-block:: bash

   pip install mercurial
   sudo apt-get install mercurial
   pip install -e hg+https://bitbucket.org/offline/django-annoying/#egg=django_annoying
