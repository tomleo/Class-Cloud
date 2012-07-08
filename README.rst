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

6. you should install django via pip::

    pip install django
    pip install django-registration
    
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
