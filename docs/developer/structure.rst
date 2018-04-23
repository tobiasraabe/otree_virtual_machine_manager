Structure
=========

The tree structure of ovmm currently looks like this::

    otree_virtual_machine_manager
    ├───docs
    │
    ├───ovmm
    │   │   cli.py
    │   │   __init__.py
    │   │
    │   ├───commands
    │   │
    │   ├───config
    │   │
    │   ├───handlers
    │   │
    │   ├───prompts
    │   │
    │   ├───static
    │
    └───tests


In this view, we have only included the most relevant parts and cover each part
separately in the following sections.

OVMM
----

.. code-block:: shell

    otree_virtual_machine_manager
    ├───ovmm
    │   │   cli.py
    │   │   __init__.py
    │   │
    │   ├───commands
    │   │   │   add_user.py
    │   │   │   backup_user.py
    │   │   │   count_user.py
    │   │   │   delete_user.py
    │   │   │   initialise.py
    │   │   │   list_user.py
    │   │   │   route_port.py
    │   │   │   upgrade_statics.py
    │   │   │   __init__.py
    │   │
    │   ├───config
    │   │   │   environment.py
    │   │   │   static.py
    │   │   │   __init__.py
    │   │
    │   ├───handlers
    │   │   │   nginx.py
    │   │   │   postgres.py
    │   │   │   samba.py
    │   │   │   __init__.py
    │   │
    │   ├───prompts
    │   │   │   defaults.py
    │   │   │   parsers.py
    │   │   │   validators.py
    │   │   │   __init__.py
    │   │
    │   ├───static
    │   │       .profile
    │   │       exp_env.7z
    │   │       nginx_default_template
    │   │       nginx_template
    │   │       otree_environ_config
    │   │       ovmm_conf.yml

``ovmm/`` contains the actual python package. On top of the folder, there
exists ``cli.py`` which is contains the command line interface. It collects all
existing commands from the folder ``commands/`` which contains one file per
command. Usually, commands require actions to be performed on the PostgreSQL,
Nginx or Samba. To provide an easy interface which automatically performs
checks for the integrity of the targeted service, handlers for these services
are included in ``handlers/``. Additionally, commands rely on prompts and
validators to receive valid user input. Pre-existing functions can be found in
``prompts/`` as well as defaults serving as examples. ``config/`` contains to
files for configuration values which can be static or dependent on the specific
environment. At last, ``static/`` contains everything which needs to be copied
to the executing account or to users accounts created by ``ovmm``.

Documentation
-------------

.. code-block:: shell

    otree_virtual_machine_manager
    ├───docs

The ``docs/`` folder contains the documentation of the project as well as this
document. New documents must be included in ``docs/index.rst`` to be compiled
as part of the documentation. Static images, etc. have to be placed in
``docs/static/``.

Tests
-----

.. code-block:: shell

    otree_virtual_machine_manager
    └───tests
        │   conftest.py
        │   test_cli.py
        │   test_handlers_postgres.py
        │   test_handlers_samba.py
        │   test_prompts_defaults.py
        │   test_prompts_parsers.py
        │   test_prompts_validators.py

The ``tests/`` folder contains the testing environment for ``ovmm`` written
with pytest. ``conftest.py`` holds variables or function which are relevant for
all tests. The other files have the following naming pattern.

1. The prefix ``test_`` is required to be automatically recognized as a file
   containing tests by pytest.
2. The middle part of the name references the subfolder of ``ovmm/`` to which
   the test file belongs. We can therefore easily see what the target of the
   test is.
3. The suffix references the specific file inside the subfolder of ``ovmm``
