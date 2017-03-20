=============================
oTree Virtual Machine Manager
=============================


.. image:: https://img.shields.io/pypi/v/otree_virtual_machine_manager.svg
        :target: https://pypi.python.org/pypi/otree_virtual_machine_manager

.. image:: https://img.shields.io/travis/tobiasraabe/otree_virtual_machine_manager.svg
        :target: https://travis-ci.org/tobiasraabe/otree_virtual_machine_manager

.. image:: https://readthedocs.org/projects/otree-virtual-machine-manager/badge/?version=latest
        :target: https://otree-virtual-machine-manager.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tobiasraabe/otree_virtual_machine_manager/shield.svg
     :target: https://pyup.io/repos/github/tobiasraabe/otree_virtual_machine_manager/
     :alt: Updates


oTree Virtual Machine Manager helps to manage user accounts.


* Free software: MIT license
* Documentation: https://otree-virtual-machine-manager.readthedocs.io.


Overview
--------

**oTree Virtual Machine Manager** is a complement to the **oTree Virtual
Machine Image** provided by Felix Albrecht and Holger Gerhardt.

Since doing research is time-consuming enough, this tool ensures that
administrators of an `oTree`_ server do not waste their time on creating fully
equipped user accounts and similar tedious tasks. Everything breaks down to
a single commandline interface.

.. _oTree: http://www.otree.org

Managing an oTree server with multiple experiments running parallel has never
been easier.


Features
--------

Create users
    Creates a fully equipped experimenter account (clear project structure,
    virtual environment, graphical or point-and-click solutions to many
    oTree-related commands, samba access).
Back up user
    Creates a database and/or home folder backup for users upon account
    closure so that nothing gets lost.
Remove user
    Removes otree-server user accounts.
Behind the scenes
    Handles port configuration for multiple parallel user accounts on a
    single virtual host.


Contributing
------------

`Contributions`_ are welcome and they are greatly appreciated! Every little
bit helps, and credit will always be given.

.. _Contributions: https://otree-virtual-machine-manager.readthedocs.io/en/latest/contributing.html#contributing


Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

