
Installation & First Steps
==========================

Python Version
--------------

Kryptonic is tested on python version 3.6 and above. Python 2 is not supported.

Driver Dependencies
-------------------

The following browsers are supported. Each one requires the official driver for programmatic control.

- **Firefox** | geckodriver_.


Installation
------------

Install the latest version of kryptonic with

.. code-block:: sh

    pip3 install kryptonic

You can quickly verify installation by running from the command line:

.. code-block:: sh

    python3 -m kryptonic

In most cases you'll a test report back (with 0 tests ran). If the command was ran in a directory with `python unittests <https://docs.python.org/3/library/unittest.html>`_, you would see those already reported with Kryptonic!

.. TODO: Add next steps. Link:
    - Writing Browser test cases
    - Typical Driver actions
    - Kryptonic Options - Configuring for multiple environments

.. _geckodriver: https://github.com/mozilla/geckodriver/releases