"""
    This module implements Yandex Translate and Dictionary APIs for Python 3.3+

    Powered by Yandex.Translate — http://translate.yandex.com/
    Powered by Yandex.Dictionary — https://tech.yandex.com/dictionary/
"""

from .config import logger

from .baseTypes import YaTranslateException, _YaAPIHandler


def Translator(*args, **kwargs):
    from .Translate import Translator
    return Translator(*args, **kwargs)


def Vocabulary(*args, **kwargs):
    from .Dictionary import Dictionary as Vocabulary
    return Vocabulary(*args, **kwargs)


def Predictor(*args, **kwargs):
    from .Prediction import Predictor
    return Predictor(*args, **kwargs)


__all__ = ["Vocabulary", "Translator", "YaTranslateException", "Predictor"]
