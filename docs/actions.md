# Basic actions with kryptonium

Kryptonium automatically binds all selenium methods to the `self.driver` instance in a test suite. Additionally, there are higher-order methods that make testing simpler and more readable.

There are many actions you can take on a web page. We will cover the following five common actions.

1. Select an element
1. Enter text in an element
1. Click an element
1. Refresh the page
1. Wait

## Selecting an element

There are many ways to select an element, and all methods are bundled in the `wait_for_element` method.

```python
self.driver.wait_for_element(id='special-element')
self.driver.wait_for_element(css_selector='#special-element.special-class')
self.driver.wait_for_element(class_name='special-class')
self.driver.wait_for_element(link_text='click')
self.driver.wait_for_element(xpath="//button[@class='special-class']")
```

Using more than one of the keyword argument will raise a `ValueError`

```python
self.driver.wait_for_element(id='special-element', link_text='click')

# ValueError: wait_for_element must use one kwarg of: css_selector, class_name, xpath, link_text
```

A `KrWebElementWrapper` is returned when the element is found. This is a wrapper around a Selenium WebElement.

#### Optinal Beheivor

**Timeouts** - `wait_for_element` will wait for 20 seconds by default before raising a timeout exception. The wait time can be changed with the `timeout` kwarg.

```python
self.driver.wait_for_element(id='must-appear-quickly', timeout=2)  # will wait 2 seconds.
```

**Optional Elements** - Sometimes it is desirable to proceed even when an element does not appear (such as a cookie alert that only happens once). An `optional` kwarg can be set to true to prevent timeout exceptions.

When `optional` is set to `True`, if the timeout is reached, a warning is logged, and the method returns a special `KrMissingElement`, which can be interacted with in the same way `KrWebWelementWrapper`s can. Calls on this method will have no effect.

```python
el = self.driver.wait_for_element(id='announcement', optional=True)
el.click() # no effect if missing
```

## Enter text in an element.

`self.wait_for_element` returns the web element directly, so it can be interacted with using `send_keys`

```python
self.driver.wait_for_element(id='username').send_keys('nick@untapt.com')
```

#### Special Keys

non-character keys (such as Enter) can be imported from `kryptonium.keys`.

```python
from kryptonium.keys import Keys
self.driver.wait_for_element(id='username').send_keys(
                                                    'nick@untapt.com',
                                                    Key.TAB)

```

## Click an element

Elements can be clicked on using the `click()`

```python
el.click()
```

## Refresh the page

A method exists on the `driver` instance

```python
self.driver.refresh()
```

## Wait

For convenience, a `wait` method exists on elements

```python
el = self.driver.wait_for_element(id='foo')
el.wait(10)
el.click()
```

This is particularly useful when chaining methods (see below). When chaining is not nescessary, or if there's no element in the current line of execution, the python built-in `time.sleep` can be used.

Note that `KrMissingElement`s will not honor its `wait` call, and `time.sleep` is a better use in these situations.

```python
self.driver.wait_for_element(id='may-not-exist').click()
time.sleep(10)
```

## Chainable methods

Most of `KrWebElementWrapper`s return its own instance, allowing the ability to chain methods. This creates a more declarative look to test suites

```python
self.wait_for_element(id='password').click().wait(3).send_keys(os.environ['PASSWORD'], Keys.ENTER)
```