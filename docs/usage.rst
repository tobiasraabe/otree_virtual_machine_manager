=====
Usage
=====


.. _general_usage:

General usage
-------------

Always run ``otree_ubuntu_server_manager`` with ``sudo`` or some commands might not work.

If you need more information on the commands, run ``otree_ubuntu_server_manager --help``


.. _first_run:

First run
---------

When using ``otree_ubuntu_server_manager`` for the first time, run ``sudo otree_ubuntu_server_manager initialise`` to set up you system.

The command performs the following actions:

- Installing Ubuntu dependencies
- Installing a settings file

After running the command, there is a folder called ``/home/<user>/ousm/`` which contains ``ousm_settings.py``. Perform two checks: first, check whether the login information for the PostgreSQL database is correctly set. Next, define the ranges of port numbers in ``POSTGRES_MISC``. The dictionary keys contain python lists. Insert distinct values or use list comprehension for bigger ranges.


.. _commands:

Commands
--------

.. automodule:: otree_ubuntu_server_manager.commands.initialise
    :members:

.. automodule:: otree_ubuntu_server_manager.commands.add_user
    :members:

.. automodule:: otree_ubuntu_server_manager.commands.backup_user
    :members:

.. automodule:: otree_ubuntu_server_manager.commands.count_user
    :members:

.. automodule:: otree_ubuntu_server_manager.commands.delete_user
    :members:

.. automodule:: otree_ubuntu_server_manager.commands.list_user
    :members: