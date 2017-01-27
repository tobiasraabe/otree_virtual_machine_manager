=====
Usage
=====


.. _general_usage:

General usage
-------------

Always run ``ovmm`` with ``sudo`` or some commands might not work.

If you need more information on the commands, run ``ovmm --help``


.. _first_run:

First run
---------

When using ``ovmm`` for the first time, run ``sudo ovmm initialise`` to set up
you system.

After running the command, there is a folder called
``/home/<user>/ovmm_sources/`` which contains ``ovmm_settings.py``. Perform
two checks:
#. Check whether the login information for the PostgreSQL database is
correctly set.
#. Define the ranges of port numbers in ``POSTGRES_MISC``. The dictionary
keys contain python lists. Insert distinct values or use list
comprehension for bigger ranges.


.. _commands:

Command line options
--------------------

Command line options are entered used with ``sudo ovmm <command>``


Commands
~~~~~~~~

Since command expansion is implemented, the commands after the forward slash
are also available.

initialise / i
    Adjusts your system to the needs of ``ovmm``. It installs Ubuntu
    dependencies as well as configuration files for the Administrator.

    .. warning::
        #. This command should be executed in advance of any other command.
        #. An internet connection is needed

add_user / a
    Adds a new user to the configuration. Several prompts will ask you about
    user specific information. Please, fill out the forms in accordance with
    the provided examples.

delete_user / d
    Deletes a user from the configuration. Her account including her home
    folder is completely removed. Make sure you have a backup of all files in
    advance.

backup_user / b
    Creates a database backup for a given user and saves it in the
    administrator's home directory under
    ``/home/<admin>/ovmm_sources/user_backups``.

count_user / c
    Returns the number of existing accounts and the number of possible,
    additional accounts.

list_user / l
    Gives a list of user names of all currently installed users.


.. _end_user_commands:

End User Commands
-----------------

Apart from the standard otree commands, the user has the following commands
at hand:

* ``run_mail_prodserver`` starts a production server and notifies the
  user via email if the server crashes.

* ``run_prodserver`` starts a production server (without notification,
  not advised except for testing).

The user should not run ``otree runserver`` (which is just for local testing)
or ``otree runprodserver`` (because of the proxy settings).


.. _running_experiments:

Running Experiments as End User
-------------------------------

As End User you have to follow the following steps in order to run
experiments.

1. Do you want or need to reset your database?
    ``otree resetdb``

2. Set the otree environment variable to Production
    ``OTREE_PRODUCTION=1; export OTREE_PRODUCTION``.

3. Start the Server either by running ``run_mail_prodserver`` or
   ``run_prodserver``.
