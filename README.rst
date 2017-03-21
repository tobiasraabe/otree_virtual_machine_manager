=============================
oTree Virtual Machine Manager
=============================


.. image:: https://img.shields.io/pypi/v/ovmm.svg
    :target: https://pypi.python.org/pypi/ovmm

.. image:: https://travis-ci.org/tobiasraabe/otree_virtual_machine_manager.svg?branch=master
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

**oTree Virtual Machine Manager** is a complement to the
`oTree Virtual Machine Image`_ provided by Felix Albrecht and
Holger Gerhardt.

.. _oTree Virtual Machine Image: https://uni-bonn.sciebo.de/index.php/s/0W9NFn2WfFSidx6

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


Tutorials
---------

You can find a series of tutorial videos on `Youtube`_.

.. _Youtube: https://www.youtube.com/playlist?list=PLLsWdtzzDdAS3c7mQi6DmlPTV4Kiw-sqB

**For administrators**:

- `Installation of ovmm`_
- `Adding a user account with ovmm`_
- `Restoring a database`_

.. _Installation of ovmm: https://youtu.be/CVh-BO2u-ak?list=PLLsWdtzzDdAS3c7mQi6DmlPTV4Kiw-sqB
.. _Adding a user account with ovmm: https://youtu.be/9hC9an9jtYc?list=PLLsWdtzzDdAS3c7mQi6DmlPTV4Kiw-sqB
.. _Restoring a database: https://youtu.be/bKkgbmnaJvk?list=PLLsWdtzzDdAS3c7mQi6DmlPTV4Kiw-sqB

**For end users**:

- `Using ovmm as an end user`_
- `Resetting the database and backups as end user`_

.. _Using ovmm as an end user: https://youtu.be/IfGKPigrOew?list=PLLsWdtzzDdAS3c7mQi6DmlPTV4Kiw-sqB
.. _Resetting the database and backups as end user: https://youtu.be/p3VmxNWIO0k?list=PLLsWdtzzDdAS3c7mQi6DmlPTV4Kiw-sqB



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

