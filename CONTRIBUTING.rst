.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at
https://github.com/tobiasraabe/otree_virtual_machine_manager/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with
"FEATURE_REQUEST", "FEATURE_IDEA" and "HELP_WANTED" is open to whoever wants to
implement it.

Furthermore, have a look at :doc:`structure` to see how your
implementation fits into the current design of ovmm.

Write Documentation
~~~~~~~~~~~~~~~~~~~

oTree Virtual Machine Manager could always use more documentation, whether as
part of the official oTree Virtual Machine Manager docs, in docstrings, or
even on the web in blog posts, articles, and such.

If you want to participate by writing docstrings, please, follow the guidelines
for `NumPy Style Python Docstrings
<http://www.sphinx-doc.org/en/1.5.2/ext/napoleon.html>`_. For a complete
example, follow this link (`Example NumPy Docstring
<http://www.sphinx-doc.org/en/1.5.2/ext/example_numpy.html#example-numpy>`_).

A more general tutorial for reStructuredText can be found
`here <http://docutils.sourceforge.net/docs/user/rst/demo.txt>`_.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/tobiasraabe/otree_virtual_machine_manager/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `ovmm` for local development.

1. Fork the `ovmm` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/ovmm.git

3. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed, this is how you set up your fork for local
   development::

    $ mkvirtualenv ovmm
    $ cd ovmm/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass all the tests
   defined with tox::

    $ tox

   You can test separately by typing::

    $ tox -e ${TOXENV}

   The following commands test python code and documentation::

    $ tox -e flake8
    $ tox -e doc8

   If you want to lint code and documentation, type::

    $ tox -e linters

   To get flake8, tox, doc8, restructuredtext_lint just pip install them into
   your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.4, 3.5 and 3.6, and for PyPy.
   Check https://travis-ci.org/tobiasraabe/otree_virtual_machine_manager/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

$ py.test tests.test_otree_virtual_machine_manager

