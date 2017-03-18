=====
Usage
=====


.. _general_usage:

General usage
-------------

``ovmm`` is a complement to the **oTree Virtual Machine Image** provided by
Felix Albrecht and Holger Gerhardt. Therefore, until now it is only tested on
this specific image. But, we do provide information (:ref:`requirements`) on
how to create a similar image which can use ``ovmm``.

Always run ``ovmm`` with ``sudo`` or some commands might not work.

If you need more information on the commands, run ``ovmm --help``


.. _first_run:

First run
---------

#. When using ``ovmm`` for the first time, run ``sudo ovmm initialise`` to
   configure your system.

    .. note:: The process leads you through the installation of required
              dependecies and creates necessary content files for ``ovmm``.

              #. Enter administrator's password.
              #. Enter account information of the PostgreSQL superuser.

                 By default, the superuser for a PostgreSQL database is called
                 ``postgres``. You also have to set a password for this
                 account. This password can be new and will be set to the user
                 by request.


#. After running the command, there is a folder called
   ``/home/<user>/ovmm_sources/`` which contains ``ovmm_conf.yml``.
   Perform the following checks:

    #. Check whether the login information for the PostgreSQL database is
       correctly set.
    #. Define the ranges of port numbers, e.g. ``OVMM_DAPHNE_RANGE``. Port
       ranges are stored in lists. Insert distinct values or use list
       comprehension for bigger ranges.


#. Next, go back to your home folder. You should see a file called
   ``nginx_template``. Read the commentary to adjust the file to your network
   configuration.

   This file will be reused every time a new user is created. The process will
   fill out the user specific values and place it under
   ``/etc/nginx/sites-avalaible``. Then, a symlink will link this file to
   ``/etc/nginx/sites-enabled``, so that `Nginx`_ takes care of it.

   .. _Nginx: https://nginx.org/en/


#. Forelast, try out one of the innocent lookup commands like
   ``sudo ovmm count_user`` or ``list_user``. If they succeed, you have
   correctly set up ``ovmm``.


#. Last, set up a test account and verify whether everything is working
   including *oTree* by running one of the example experiments.




.. _command_line_options:

Command line options
--------------------

Command line options are entered used with ``sudo ovmm <command>``


.. _commands:

Commands
~~~~~~~~

Since command expansion is implemented, the commands after the forward slash
are also available.

initialise / i
    Adjust your system to the needs of ``ovmm``. It installs Ubuntu
    dependencies as well as configuration files for the Administrator.

    .. warning::
        #. This command should be executed on first run in advance of any other
           command.
        #. An internet connection is needed

add_user / a
    Add a new user to the configuration. Several prompts will ask you about
    user specific information. Please, fill out the forms in accordance with
    the provided examples.

delete_user / d
    Delete a user from the configuration. Her account including her home
    folder is completely removed. Make sure you have a backup of all files in
    advance.

backup_user / b
    Create a backup for a given user and save it in the
    administrator's home directory under
    ``/home/<admin>/ovmm_sources/user_backups``. Choose from one of three
    options, ``all``, ``db``, ``home``, whether you want to make a backup of
    the database or the home folder. ``all`` is a shortcut to run a backup of
    both, database and home folder.

count_user / c
    Return the number of existing accounts and the number of possible,
    additional accounts.

list_user / l
    Give a list of user names of all currently installed users.


