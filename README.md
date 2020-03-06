# kryptonic - function test library for the kryptonic environment.

## Setup

## Introduction

Pytonic is an extension of the builtin `unittest` module, and introduces Selenium bindings and a suite of new plain-english methods. Writing a test suite is the same as with `unittest`

Where a `unittest` test case might look like:

```python
from unittest import TestCase

class TestMath(TestCase):

    def test_can_add(self):
        self.assertEqual(1+1, 2)

```

```python
from kryptonic import KrTestCase

class TestMath(KrTestCase):

    def test_can_add(self):
        self.assertEqual(1+1, 2)
```

Pytonic tests can be ran from the command line, in a similar way to unittest:

```shell
$ python -m kryptonic
```

This tells kryptonic to search for all tests suites from the current directory.

### Selenium webdriver

In addition to the usual test methods bound to `self`, a selenium webdriver (default Firefox) is setup to be used within the test suite. By default every test suite opens a new browser controlled by `self.driver`.

`self.driver` has a number of higher order methods that abstract many selenium bindings. The goal is that in a test suite, all webdriving can be easily achieved without the need to import extra `selenium` packages.

```python
class Test(KrTestCase):

    def test_visit_google(self):
        self.driver.get('https://google.com')
        self.assertEqual('Google', self.driver.title)

```

## Test running in python scripts

You can run test suites in ways similar to unittest. For example, to write a script that tests upon execution

```python
import kryptonic

class Test(kryptonic.KrTestCase):

    def test_visit_google(self):
        self.driver.get('https://google.com')
        self.assertEqual('Google', self.driver.title)
        
    def test_search(self):
        self.driver.get('https://google.com')
        element = self.driver.wait_for_element(css_selector='#search')
        element.send_keys("Test the search bar")
        

if __name__ == '__main__':
    kryptonic.main()

```


## Configuration (config options)

A number of options can be configued at the global or individual level. They are defined upon running unittests, and can be passed in a number of ways. The following examples will use the cli `--config-args` method to set the options.

### Opening test browsers to a predefined url.

In many cases, each test suite needs to navigate to the same url. Usually, you would need to invoke a `driver.get` to achieve this. Consider the following:

```python

class Test(KrTestCase):

    def test_login(self):
        self.driver.get('https://example.com')
        self.driver.wait_for_element(link_text='login').click()
    
    def test_admin(self):
        self.driver.get('https://example.com/admin')
        self.driver.wait_for_element(css_selector='#admin-panel', timeout=5)
        
    def test_tos(self):
        self.driver.get('https://example.com')
        self.driver.wait_for_element(link_text='terms').click()
        self.assertEqual('Terms of Service', self.driver.title)
```

Each test suite navigates to the same url. This can be automated by setting the `url` option to a default location to visit:

```shell
python -m kryptonic --config-args url=https://example.com
```

When running in this way, the previous test suites can be refactored to:

```python
class Test(KrTestCase):

    def test_login(self):
        self.driver.wait_for_element(link_text='login').click()
    
    def test_admin(self):
        self.driver.get_path('/admin')
        self.driver.wait_for_element(css_selector='#admin-panel', timeout=5)
        
    def test_tos(self):
        self.driver.wait_for_element(link_text='terms').click()
        self.assertEqual('Terms of Service', self.driver.title)
```

Because each browser will open to `https://example.com` by default, there's no need to navigate there manually (note the change in the second suite to use `driver.get_path` to get a particular route following the domain)

Use of the `url` config option saves on typing and can also be utilized to change when testing in different environments.
 
### Setting config

Config can be set in the following ways, and each way a config is set has a certain prescedence. From least prescedence to most precidence:

#### Environment Variables (0)

The name of an option prefixed with `KR_`

```shell
KR_URL=http://localhost:5000
KR_CUSTOM_OPTION=1
```

#### Passing a dict to kryptonic.main (1)

```python3
from kryptonic import kryptonic

kryptonic.main(config={
    'url': 'http://localhost:5000',
    'custom_option': 1
})
```

#### Setting a Test Suite's `config` attribute (2):

```python3
from kryptonic import KrFirefox

class TestFoo(KrFirefox):
    
    config = {
    'url': 'http://localhost:5000',
    'custom_option': 1
    }

```

#### Invoking the  `--config-args` option in the cli (3):

```shell
python -m kryptonic discover --config-args url=http://localhost:5000,custom_option=1
```

#### 

## Testing hooks (setup, teardown)

Kryptonic mimick the `unittest.TestCase` `setUp` and `tearDown` methods.