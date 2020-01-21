# pytonium - function test library for the kryptonium environment.

## Setup

## Configuration (config options)

A number of options can be configued at the global or individual level. They can be defined in the following ways, from least prescedence to most precidence:

#### Environment Variables (0)

The name of an option prefixed with `KR_`

```shell
KR_URL=http://localhost:5000
KR_CUSTOM_OPTION=1
```

#### Passing a dict to pytonium.main (1)

```python3
from pytonium import pytonium

pytonium.main(config={
    'url': 'http://localhost:5000',
    'custom_option': 1
})
```

#### Setting a Test Suite's `config` attribute (2):

```python3
from pytonium import KrFirefox

class TestFoo(KrFirefox):
    
    config = {
    'url': 'http://localhost:5000',
    'custom_option': 1
    }

```

#### Invoking the  `--config` option in the cli (3):

```shell
python -m pytonium discover --config url=http://localhost:5000,custom_option=1
```

#### 

## Testing hooks (setup, teardown)

Pytonium mimick the `unittest.TestCase` `setUp` and `tearDown` methods.