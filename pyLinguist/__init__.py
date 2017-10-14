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

from .mixins import YaBaseAPIHandler
from .exc import YaTranslateException
from .utils import Logger


def Translator(api_key: str, xml: bool=False, version: str='1.5'):
    from .Translate import Translator
    return Translator(api_key=api_key, xml=xml, version=version)


def Dictionary(api_key: str, xml: bool=False, version: str='1'):
    from .Vocabulary import Dictionary
    return Dictionary(api_key=api_key, xml=xml, version=version)


def Predictor(api_key: str, xml: bool=False, version: str='1'):
    from .Prediction import Predictor
    return Predictor(api_key=api_key, xml=xml, version=version)


def Speller(xml: bool=False, encoding: str='utf-8', **kwargs):
    from .Vocabulary import Speller
    return Speller(xml=xml, encoding=encoding, **kwargs)


__all__ = ["Dictionary", "Translator", "YaTranslateException",
           "Predictor", "Speller"]
__author__ = "Dmitry Pchelkin"
__version__ = (0, 1, 3)
