# helenium

## What is it?

It is very tedious to download chromedriver whenever your chrome browser get updated, or if you want to setup new environment. This package handles downloading chormedriver automatically. In addition, it also gives you some handy selenium wrapper class.

## Installation

Use pip to install this package. It is not yet released in Pypi, but it is planned to do so when the version reached 1.0.0!

```bash
pip install helenium
```

## How to use it?

You can import `SeleniumLoader` class if you just want to use chromedriver feature. And instantiating this will trigger setup chromdriver.

```python
from helenium import SeleniumLoader


SeleniumLoader()
```

If you want to use wrapper class,

```python
import time

from helenium.base import SeleniumBase

selenium_base = SeleniumBase()
selenium_base.setup_driver() # Same as SeleniumLoader())

selenium_base.driver.get('https://google.com')
selenium_base.click_and_send_key(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
    'Python\n',
)
time.sleep(1)

assert selenium_base.driver.current_url.startswith(
    'https://www.google.com/search?q=Python'
)

```
