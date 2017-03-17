.. highlight:: shell

============
Installation
============

As **oTree Virtual Machine Manager** provides useful commands to
administrators of the **oTree Virtual Machine Image**, it requires superuser
rights to perform its actions. Therefore, install ``ovmm`` under the provided
administrator account.

.. _requirements:

Requirements
------------

The following components need to be present on your system to use ``ovmm``:

:ftp:
    required for ftp access to the account
:git:
    version control
:nginx:
    webserver
:postgresql:
    database server + development packages
:pip:
    package manager for Python
:python3-venv:
    virtual environment for Python 3
:redis-server:
    remote dictionary server
:samba:
    Windows share access
:screen:
    detachable consoles
:mailutils:
    sending mails if otree stops unexpectedly
:ssh:
    remote shell access
:ufw:
    firewall
:zenity:
    GTK 3.0 dialog handler

In most Debian based Linux environments you can install these packages from the
repositories like so:

.. code-block:: console


    $ sudo apt install ftp nginx samba screen mailutils ssh ufw postgresql git  \
                       postgresql-server-dev-all python3-pip zenity             \
                       python3-venv

Please see the documentation of your Linux distribution for help.


Stable release
--------------

To install oTree Virtual Machine Manager, run this command in your terminal:

.. code-block:: console

    $ pip3 install ovmm

This is the preferred method to install oTree Virtual Machine Manager, as it
will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can
guide you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for oTree Virtual Machine Manager can be downloaded from the
`Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/tobiasraabe/otree_virtual_machine_manager

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/tobiasraabe/otree_virtual_machine_manager/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python3 setup.py install


.. _Github repo: https://github.com/tobiasraabe/otree_virtual_machine_manager
.. _tarball: https://github.com/tobiasraabe/otree_virtual_machine_manager/tarball/master

