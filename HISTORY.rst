=======
History
=======

All notable changes to this project will be documented in this file.

The format is based on `Keep A Changelog`_ and this project adheres to
`Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/spec/v2.0.0.html
.. _Keep A Changelog: http://keepachangelog.com/en/1.0.0/

Unreleased
----------
- Overhauled CLI
    - new command: upgrade_statics
    - version flag with ``ovmm --version``
    - Check for sudo when calling ``ovmm`` with error message
    - Added switch to assign user to sudo group during creation
- Separated settings into a static and environment dependent part
- Open ftp and samba ports with ufw during initialisation
- ``ovmm init`` detects whether nginx templates exists and asks before
  overwriting
- Miscellaneous
    - New format for HISTORY.rst
    - More information in python header file
    - Added credits
    - Enhanced Github PR template
    - Small adjustements to documentation tests and build


0.2.2 (2017-07-21) [YANKED]
---------------------------
* Hotfix for v0.2.1 due to error on initialise.


0.2.1 (2017-07-16)
------------------
* Re-released v0.2.0.


0.2.0 (2017-07-16)
------------------

Added
~~~~~

* ``route_port`` command to change standard ports to a different user. (Thanks,
  Felix)


0.1.1 (2017-03-20)
------------------
* Alpha release. Re-released on PyPI :).


0.1.0 (2017-03-20)
------------------
* Alpha release. Released on PyPI.
