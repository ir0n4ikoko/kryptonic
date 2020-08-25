Kryptonic.driver common browser actions
***************************************

Generally, in browser automation, there are a few actions frequently used. This page outlines the most frequent actions and their corrosponding method on Kryptonic's ``driver`` instance. These actions include:

- Navigating to a URL
- Selecting an element
- Clicking an element
- Entering text
- Refreshing the page
- Waiting

Initial setup for all examples
==============================

Each example assumes it's running a method within a kryptonic test suite. In other words:

.. code-block:: python
    :emphasize-lines: 6

    import kryptonic

    class TestCase(kryptonic.KrFirefox):

        def test_example(self):
            # EXAMPLE STARTS HERE

Navigating to a URL
===================

.. code-block:: python
    self.driver.get('example.com')

Selecting an element
====================


There are many ways to select an element, and all methods are bundled in the ``wait_for_element`` method

.. code-block:: python
    self.driver.wait_for_element(id='special-element')
    self.driver.wait_for_element(css_selector='#special-element.special-class')
    self.driver.wait_for_element(class_name='special-class')
    self.driver.wait_for_element(link_text='click')
    self.driver.wait_for_element(xpath="//button[@class='special-class']")

Note that using more than one of the keyword argument will raise a ``ValueError``:

.. code-block:: python
    self.driver.wait_for_element(id='special-element', link_text='click')
    # ValueError: wait_for_element must use one kwarg of: css_selector, class_name, xpath, link_text


A ``KrWebElementWrapper`` is returned when the element is found. This is a wrapper around a Selenium WebElement.

Optional Beheivor
-----------------

**Timeouts** - wait_for_element will wait for 20 seconds by default before raising a timeout exception. The wait time can be changed with the timeout kwarg.

.. code-block:: python

    self.driver.wait_for_element(id='must-appear-quickly', timeout=2)  # will wait 2 seconds.


Optional Elements - Sometimes it is desirable to proceed even when an element does not appear (such as a cookie alert that only happens once). An optional kwarg can be set to true to prevent timeout exceptions.

When optional is set to ``True``, if the timeout is reached, a warning is logged, and the method returns a special ``KrMissingElement``, which can be interacted with in the same way KrWebWelementWrappers can. Calls on this method will have no effect.

.. code-block:: python

    el = self.driver.wait_for_element(id='announcement', optional=True)
    el.click() # no effect if missing

