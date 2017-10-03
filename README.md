# pyLinguist

[![Build Status](https://travis-ci.org/hell03end/pyLinguist.svg?branch=master)](https://travis-ci.org/hell03end/pyLinguist)
[![PyPI version](https://badge.fury.io/py/pyLinguist.svg)](https://badge.fury.io/py/pyLinguist)
[![Dependency Status](https://gemnasium.com/badges/github.com/hell03end/pyLinguist.svg)](https://gemnasium.com/github.com/hell03end/pyLinguist)

Library for Yandex Linguistics APIs for Python 3.3+

Include:
* [Yandex Translate API](https://tech.yandex.com/translate/)
* [Yandex Dictionary API](https://tech.yandex.com/dictionary/)
* [Yandex Predictor API](https://tech.yandex.ru/predictor/)
* [Yandex Speller API](https://tech.yandex.ru/speller/)

### [Download](https://github.com/hell03end/pyLinguist/releases/download/0.1.2/pyLinguist-0.1.2.tar.gz)

### Installation
`pip install pyLinguist`

Or from sources:
```bash
git clone https://github.com/hell03end/pyLinguist.git
cd pyLinguist
python3 tests/__init__.py  # to check all work correct
```

### [Examples](https://github.com/hell03end/pyLinguist/wiki/Examples)

### Changelog
* 0.1.3:
    * add docstrings inheritance
    * add api key status cache for `.ok()` method
    * add logger
    * internal refactoring
    * move from unittest for pytest

* 0.1.3rc1:
    * remove requests from dependencies
    * use native unittest assert methods
    * TODO: change comments and documentation

* 0.1.2:
    * add Speller for grammar check
    * change Vocabulary class to Dictionary as is in Yandex API

Powered by Yandex
