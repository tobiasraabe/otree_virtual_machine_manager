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

The command performs the following actions:

- Installing Ubuntu dependencies
- Installing a settings file

After running the command, there is a folder called ``/home/<user>/ovmm/``
which contains ``ovmm_settings.py``. Perform two checks: first, check whether
the login information for the PostgreSQL database is correctly set. Next,
define the ranges of port numbers in ``POSTGRES_MISC``. The dictionary keys
contain python lists. Insert distinct values or use list comprehension for
bigger ranges.


.. _commands:

Commands
--------

.. automodule:: ovmm.commands.initialise
    :members:

.. automodule:: ovmm.commands.add_user
    :members:

.. automodule:: ovmm.commands.backup_user
    :members:

.. automodule:: ovmm.commands.count_user
    :members:

.. automodule:: ovmm.commands.delete_user
    :members:

.. automodule:: ovmm.commands.list_user
    :members:
    
    
End User Commands
-----------------

Apart from the standard otree commands, the user has the following commands at hand:

* ```run_mail_prodserver```, starts a production server and notifies the user via email if the server crashes. 

* ```run_prodserver```, starts a production server (without notification, not advised except for testing).

The user should not run ```otree runserver``` (which is just for local testing) or ```otree runprodserver```(because of the proxy settings)

Running Experiments as End User
-------------------------------

As End User you have to follow the following steps in order to run experiments.

1. Do you want or need to reset your database?
    ```otree resetdb``

2. Set the otree environment variable to Production
    ```OTREE_PRODUCTION=1; export OTREE_PRODUCTION```
  
3. Start the Server either by running ```run_mail_prodserver``` or ```run_prodserver```
