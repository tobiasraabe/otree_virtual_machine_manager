.. highlight:: shell

============
Installation
============

As **oTree Virtual Machine Manager** provides useful commands to
administrators of the **oTree Virtual Machine Image**, it requires superuser
rights to perform its actions. Therefore, install ``ovmm`` under the provided
administrator account.


.. _images:

Preconfigured Systems
---------------------

We created a Virtualbox image for oTree users based on **ovmm** and on "Ubuntu
16.04.2 Server 64bit" and comes with three desktops *Gnome*, *LXDE*, and
*fluxbox* to allow it to work on systems with varying level RAM.

The images all contain a user account called ``otreeadmin`` that comes
preconfigured with the set of end user commands provided by **ovmm**. The
images further each contain an account ``ovmmadmin`` from where **ovmm** can be
used to create more accounts.

You find the images here: `oTree Virtual Machine Images`_

.. _oTree Virtual Machine Images: https://uni-bonn.sciebo.de/index.php/s/0W9NFn2WfFSidx6

We also spent some time on trying to figure out what tools could be useful
to the end users. Therefore all images with the following tools preinstalled.

:Chromium:
  Webbrowser
:Giggle:
  GUI for Git,
:Atom:
  Great free IDE with many plugins,
:pgAdmin 3:
  GUI for postreSQL database systems


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
:xterm:
    Linux terminal emulator
:zenity:
    GTK 3.0 dialog handler

In most Debian based Linux environments you can install these packages from the
repositories like so:

.. code-block:: console


    $ sudo apt install ftp nginx samba screen mailutils ssh ufw postgresql git  \
                       postgresql-server-dev-all python3-pip zenity             \
                       python3-venv redis-server xterm

Please see the documentation of your Linux distribution for help.


Stable release
--------------

To install oTree Virtual Machine Manager, run this command in your terminal:

.. code-block:: console

    $ sudo pip3 install ovmm

This is the preferred method to install oTree Virtual Machine Manager, as it
will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can
guide you through the process.

.. _pip: https://pip.pypa.io/en/stable/
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

    $ sudo python3 setup.py install


.. _Github repo: https://github.com/tobiasraabe/otree_virtual_machine_manager
.. _tarball: https://github.com/tobiasraabe/otree_virtual_machine_manager/tarball/master

.. _software_recommendations:

Recommendations for Additional Software
---------------------------------------

To enhance the working experience for the oTree end user we recommend to also
install the following software packages.

:chromium:
   Chromium browser is the Open Source version of Chrome browser. As it is the
   most frequently used browser on the web it is the recommended testing
   environment for your oTree apps.

:conky:
   Desktop system monitor.
   ovmm statics provides a preconfigured conky configuration file which is
   unzipped into the user's $HOME directory and provides helpful system
   information while running oTree.

:Atom:
   Open Source IDE with many features.

:pgAdmin III:
   Graphical user interface for postgreSQL database servers. Helps with
   understanding oTree and data recovery if something goes wrong.


In Ubuntu and official derivatives you can install chromium, conky, and pgAdmin
via the package manager, like so:

.. code-block:: console

    $ sudo apt-get install conky-all chromium-browser pgadmin3


It is recommended to obtain LightTable from the official website as the
community packages are deprecated.

You can find the website here: http://lighttable.com

