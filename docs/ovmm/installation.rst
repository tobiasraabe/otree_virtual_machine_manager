
.. _ovmm_installation:

Installation
============

The following steps guide you through the installation process of OVMM.

OVMM
----

To install oTree Virtual Machine Manager, run this command in your terminal:

.. code-block:: console

    $ sudo pip install ovmm

This is the preferred method to install oTree Virtual Machine Manager, as it
will always install the most recent stable release.

.. note::

    Sometimes it might be necessary to install a different version than the one
    provided on `PyPI`_.

    .. _PyPI: https://pypi.org/project/ovmm/

    If you want to install a different version of OVMM, run

    .. code-block:: console

        $ sudo pip install ovmm==0.2.2

    If you want to install a version from a Github branch called ``tweaks``,
    run

    .. code-block:: console

        $ sudo pip install git+https://github.com/tobiasraabe/otree_virtual_machine_manager@tweaks

    (This command was especially useful in this `example`_ where a fix needed
    to be tested quickly.)

    .. _example: https://github.com/tobiasraabe/otree_virtual_machine_manager/pull/122
