# @TODO: test callbacks and proxies

import os
import unittest
import logging


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - "
                           "%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestImports(unittest.TestCase):
    def test_from_init(self):
        exceptions_happend = False
        try:
            from pyYandexLinguistics import Translator
            assert Translator
            from pyYandexLinguistics import Vocabulary
            assert Vocabulary
            from pyYandexLinguistics import Predictor
            assert Predictor
            from pyYandexLinguistics import YaTranslateException
            assert YaTranslateException
        except ImportError as err:
            logger.debug(err)
            exceptions_happend = True
        assert not exceptions_happend

    def test_from_modules(self):
        exceptions_happend = False
        try:
            from pyYandexLinguistics import Translate
            assert Translate and Translate.Translator
            from pyYandexLinguistics import Dictionary
            assert Dictionary and Dictionary.Dictionary
            from pyYandexLinguistics import Prediction
            assert Prediction and Prediction.Predictor
        except ImportError as err:
            logger.debug(err)
            exceptions_happend = True
        assert not exceptions_happend


from pyYandexLinguistics import (
    Translator, Vocabulary, Predictor, YaTranslateException
)


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_TRANSLATE")
        assert self.api_key
        self.t = Translator(self.api_key)
        assert self.t.ok  # check api key is correct

    def test_get_langs(self):
        langs = self.t.get_langs()
        assert langs and isinstance(langs, dict)
        assert 'dirs' in langs
        assert self.t._cache
        self.t._cache = None
        langs = self.t.get_langs()
        assert langs and self.t._cache

    def test_directions(self):
        langs = self.t.get_langs()
        directions = self.t.directions
        assert directions and isinstance(directions, list)
        assert directions == langs['dirs']

    def test_languages(self):
        langs = self.t.get_langs()
        languages = self.t.languages
        assert langs and isinstance(langs, dict)
        if 'langs' not in langs:
            return
        assert languages and isinstance(languages, dict)
        assert languages == langs['langs']

    def test_ok(self):
        assert self.t.ok

    def test_detect(self):
        exception_happend = False
        try:
            self.t.detect("hello", hint='en')
        except ValueError as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        guess_lang = self.t.detect("hello")
        assert guess_lang and isinstance(guess_lang, str)
        assert guess_lang == 'en'
        guess_lang = self.t.detect("gutten", hint=['de'])
        assert guess_lang and guess_lang == 'de'
        guess_lang = self.t.detect("hello", post=True)
        assert guess_lang and guess_lang == 'en'

    def test_translate(self):
        translation = self.t.translate("hello, world", 'de', options=1)
        assert translation and isinstance(translation, dict)
        assert 'code' not in translation and 'detected' in translation
        translation = self.t.translate("hello", 'en-de', options=0)
        assert translation and 'detected' not in translation


class TestVocabulary(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_DICT")
        assert self.api_key
        self.v = Vocabulary(self.api_key)
        assert self.v.ok  # check api key is correct

    def test_get_langs(self):
        langs = self.v.get_langs()
        assert langs and isinstance(langs, list)
        assert self.v._cache
        self.v._cache = None
        langs = self.v.get_langs()
        assert langs and self.v._cache

    def test_ok(self):
        assert self.v.ok

    def test_lookup(self):
        exception_happend = False
        try:
            self.v.lookup("hello", 'cpp')
        except YaTranslateException as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        definition = self.v.lookup("hello", 'en-en')
        assert definition and isinstance(definition, dict)
        assert 'head' not in definition and 'def' in definition

    def test_definitions(self):
        exception_happend = False
        try:
            self.v.definitions("hello", 'cpp')
        except YaTranslateException as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        definition = self.v.definitions("hello", 'en-en')
        assert definition and isinstance(definition, list)


class TestPredictor(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_PREDICTOR")
        assert self.api_key
        self.p = Predictor(self.api_key)
        assert self.p.ok  # check api key is correct

    def test_get_langs(self):
        langs = self.p.get_langs()
        assert langs and isinstance(langs, list)
        assert self.p._cache
        self.p._cache = None
        langs = self.p.get_langs()
        assert langs and self.p._cache

    def test_ok(self):
        assert self.p.ok

    def test_complete(self):
        exception_happend = False
        try:
            self.p.complete('cpp', "#includ")
        except YaTranslateException as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        prediction = self.p.complete('en', "hello", limit=1)
        assert prediction and isinstance(prediction, dict)
        assert 'endOfWord' in prediction and prediction['endOfWord']
        assert 'text' in prediction and len(prediction['text']) == 1
        prediction = self.p.complete('en', "hel", limit=5)
        assert prediction
        assert 'endOfWord' in prediction and not prediction['endOfWord']
        assert 'text' in prediction and len(prediction['text']) == 5


if __name__ == "__main__":
    unittest.main()
