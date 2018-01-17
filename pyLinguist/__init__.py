"""
    pyLinguist
    ==========

    Implements Yandex Linguistics APIs for Python 3.3+

    Include: Translate API, Dictionary API, Speller API, Predictor API.
    Powered by Yandex (https://tech.yandex.com).

    Usage
    -----
    from pyLinguist import Translator
    import os
    t = Translator(os.environ.get("KEY_FOR_TRANSLATOR_API"))
    assert t.ok  # check api key is correct
    t.translate("Hello", 'es')  # get simple translation
    # {'lang': 'en-es', 'detected': {'lang': 'en'}, 'text': ['Hola']}
"""

import logging

from pyLinguist.exc import YaTranslateException

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d]"
           " %(message)s",
    datefmt="%H:%M:%S"
)


def Translator(api_key: str, version: str='1.5', **kwargs):
    from pyLinguist.Translate import Translator
    return Translator(api_key=api_key, version=version, **kwargs)


def Dictionary(api_key: str, version: str='1', **kwargs):
    from pyLinguist.Vocabulary import Dictionary
    return Dictionary(api_key=api_key, version=version, **kwargs)


def Predictor(api_key: str, version: str='1', **kwargs):
    from pyLinguist.Prediction import Predictor
    return Predictor(api_key=api_key, version=version, **kwargs)


def Speller(encoding: str='utf-8', **kwargs):
    from pyLinguist.Vocabulary import Speller
    return Speller(encoding=encoding, **kwargs)


__author__ = "Dmitry Pchelkin"
__version__ = (0, 1, 3)
