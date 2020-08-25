
Installation & First Steps
==========================

Python Version
--------------

Kryptonic is tested on python version 3.6 and above. Python 2 is not supported.

Driver Dependencies
-------------------

The following browsers are supported. Each one requires the official driver for programmatic control.

- **Firefox** | geckodriver_.
- More Web browsers coming soon.


Installation
------------

Install the latest version of kryptonic with

.. code-block:: sh

    pip3 install kryptonic

You can quickly verify installation by running from the command line:

.. code-block:: sh

    python3 -m kryptonic

In most cases you'll a test report back (with 0 tests ran). If the command was ran in a directory with `python unittests <https://docs.python.org/3/library/unittest.html>`_, you would see those already reported with Kryptonic!


Browser test case example
-------------------------

As the main purpose of Kryptonic is to extend python unittest module to add browser automation, a kryptonic test follows the same structure, with unittest modules replaced by kryptonic modules.

.. code-block:: python
    :linenos:

    import kryptonic

    class SimpleTestCase(kryptonic.KrFirefox):

        config = {'cleanup': 'onsuccess'}

        def test_navigate_to_page(self):
            self.driver.get('https://example.com')
            self.assertEqual('Example Domain', self.driver.title)

    if __name__ == '__main__'
        kryptonic.main()

This code can be ran in the same way as above (with ``python -m kryptonic``), or by running the file, i.e. ``python name_of_file.py``.

A few notable parts of this example include:

- ``config`` (line 5) - alter the beheivor of kryptonic before, during and after tests. More info:
   - :doc:`config-api` - Which lists all config options.
   - :doc:`config` - Which includes different ways to pass configuration & their priority.
- ``self.driver.get`` (line 8) - One of the many higher order actions on ``driver``, which Kryptonic adds to ``self`` in each test suite. More info:
   - :doc:`common-actions` - The fundamental methods for driving browser automation.

.. TODO: Add next steps. Link:
    - Writing Browser test cases
    - Typical Driver actions
    - Kryptonic Options - Configuring for multiple environments

.. _geckodriver: https://github.com/mozilla/geckodriver/releases
