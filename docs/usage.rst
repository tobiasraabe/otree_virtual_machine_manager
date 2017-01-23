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

.. automodule:: ovmm.commands.initialise
    :members:

After running the command, there is a folder called ``/home/<user>/ovmm/``
which contains ``ovmm_settings.py``. Perform two checks: first, check whether
the login information for the PostgreSQL database is correctly set. Next,
define the ranges of port numbers in ``POSTGRES_MISC``. The dictionary keys
contain python lists. Insert distinct values or use list comprehension for
bigger ranges.


.. _commands:

Commands
--------



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
