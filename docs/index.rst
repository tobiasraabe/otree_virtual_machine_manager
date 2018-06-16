Welcome to the documentation of OVMI and OVMM!
==============================================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/tobiasraabe/otree_virtual_machine_manager/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/ovmm.svg
    :target: https://pypi.org/project/ovmm/

.. image:: https://travis-ci.org/tobiasraabe/otree_virtual_machine_manager.svg?branch=master
    :target: https://travis-ci.org/tobiasraabe/otree_virtual_machine_manager

.. image:: https://readthedocs.org/projects/otree-virtual-machine-manager/badge/?version=latest
    :target: https://otree-virtual-machine-manager.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The oTree Virtual Machine Image (OVMI) and oTree Virtual Machine Manager (OVMM)
are two pieces of software which facilitate working with oTree.

OVMI is targeted at all users of oTree and enables the user to launch an oTree
experiment without having the hassle of keeping all components and dependencies
together. In addition to that the image offers graphical interfaces for users
which are not accustomed to using the command line and need a slower
transition.

In contrast to that OVMM is directed at server administrators of research labs.
After the server is set up with OVMI and OVMM is installed, the administrator
can quickly create, delete, backup accounts for experimenters where all the
routines are reduced to one command. In the background, OVMM will take care of
the network configuration.

.. toctree::
    :caption: User Guide - OVMI
    :maxdepth: 1

    ovmi/introduction
    ovmi/installation
    ovmi/getting_started

.. toctree::
    :caption: User Guide - OVMM
    :maxdepth: 1

    ovmm/introduction
    ovmm/installation
    ovmm/getting_started

.. toctree::
    :caption: Developer Guide
    :maxdepth: 1

    developer/contributing
    developer/structure
    developer/installation

.. toctree::
    :caption: Additional Information
    :maxdepth: 1

    additional_information/authors
    additional_information/history


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
