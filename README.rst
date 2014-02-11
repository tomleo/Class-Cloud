|waffle|_

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

5. type the following in the command line::

    source ENV/bin/activate

6. you should install django via pip::

    pip install django
    pip install django-registration
    pip install django_extensions?
    pip install django-bootstrap-form
    
Setting up mail server for email based registration
===================================================

In ubuntu
---------

1. sudo apt-get install postfix mailutils
2. sudo touch /etc/postfix/generic
3. sudo touch /etc/postfix/sasl/passwd
4. cd /etc/postfix
5. sudo vim main.cf
6. sudo postmap generic
7. sudo  vim sasl/passwd
8. sudo postmap sasl/passwd
9. chown root.root sasl/passwd.db
10. chmod 600 sasl/passwd sasl/passwd.db
11. sudo /etc/init.d/postfix restart

*main.cf*::

    smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)
    biff = no
    smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
    smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
    smtpd_use_tls=yes
    smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
    smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
    myhostname = orbital-command
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases
    mydestination = orbital-command, localhost.localdomain, localhost
    relayhost = [smtp.gmail.com]:587
    mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
    mailbox_size_limit = 0
    recipient_delimiter = +
    inet_interfaces = loopback-only
    inet_protocols = all
    smtp_tls_loglevel=1
    smtp_tls_security_level=encrypt
    smtp_sasl_auth_enable=yes
    smtp_sasl_password_maps=hash:/etc/postfix/sasl/passwd
    smtp_sasl_security_options = noanonymous
    smtp_generic_maps=hash:/etc/postfix/generic

*generic*::

    tom@localhost tomjleo@gmail.com
    root@localhost tomjleo@gmail.com
    svnmanager@192.168.1.5 tomjleo@gmail.com

*sasl/passwd*::

    [smtp.gmail.com]:587 tomjleo@gmail.com:=NOT_TELLING!!!

Other things installed
======================

 - pip install mercurial
 - sudo apt-get install mercurial
 - pip install -e hg+https://bitbucket.org/offline/django-annoying/#egg=django_annoying

Acknowledgements
================

Class-Cloud makes heavy use of front-end frameworks, plugins, and themes.

django-bootstrap-form
---------------------

Using django-bootstrap-form to stylize model based form fields

https://github.com/tzangms/django-bootstrap-form

jquery-ui-bootstrap
-------------------

Using jquery-ui-bootstrap's custom theme to style the jQuery datepicker widget

 - jquery-ui-1.8.16.custom.css
 - jquery.ui.1.8.16.ie.css
 - images/*

https://github.com/addyosmani/jquery-ui-bootstrap

See stuff installed via pip for more libraries/frameworks/code

django-registration
-------------------

Made the following modification so that registered users are added to the 
student group:

in ENV/lib/python2.7/site-packages/registration/models.py I added the following::

    def create_inactive_user
        ...
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        
      + student = Group.objects.get(name='Student Users')
      + new_user.groups.add(student)
      
        new_user.save()
        ...



.. |waffle| image:: https://badge.waffle.io/tomleo/class-cloud.png
.. _waffle: http://waffle.io/tomleo/class-cloud
