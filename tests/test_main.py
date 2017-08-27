import os
import unittest
import requests
from xml.etree import ElementTree

from pyLinguist import (
    Translator, Dictionary, Predictor, Speller, YaTranslateException,
    _YaAPIHandler
)
from .config import logger
from .commons import GenericTest


class TestBaseTypes(GenericTest):
    def setUp(self):
        exception_happend = False
        try:
            __ = _YaAPIHandler(None)
        except YaTranslateException as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        self.api_key = "123"
        self.h_json = _YaAPIHandler(self.api_key)
        assert self.h_json
        self.h_xml = _YaAPIHandler(self.api_key, xml=True)
        assert self.h_xml

    def test_attrib_json(self):
        assert self.h_json._api_key
        assert self.h_json._json
        assert not self.h_json._cache
        assert not self.h_json._url

    def test_attrib_xml(self):
        assert self.h_xml._api_key
        assert not self.h_xml._json
        assert not self.h_xml._cache
        assert not self.h_xml._url

    def test__make_url(self):
        # equivalent for h_xml
        base_url = "http://google.com/"
        url = self.h_json._make_url("langs")
        assert url
        assert url == self.h_json._url + self.h_json._endpoints['langs']
        assert self.assert_exception_happend(self.h_json._make_url,
                                             KeyError, '')
        url = self.h_json._make_url('langs', base_url)
        assert url
        assert url == base_url + self.h_json._endpoints['langs']

    def test__form_params(self):
        params = {
            'a': 1,
            'b': 2
        }
        params_json = self.h_json._form_params(**params)
        assert params_json and isinstance(params_json, dict)
        assert 'key' in params_json
        assert 'a' in params_json and 'b' in params_json
        assert params['a'] == params_json['a']
        assert params['b'] == params_json['b']
        params_xml = self.h_xml._form_params(**params)
        assert params_xml and isinstance(params_xml, dict)
        assert 'key' in params_xml
        assert 'a' in params_xml and 'b' in params_xml
        assert params['a'] == params_xml['a']
        assert params['b'] == params_xml['b']
        params.update({'callback': self.generic_callback})
        params_json = self.h_json._form_params(**params)
        params_xml = self.h_xml._form_params(**params)
        assert 'callback' in params_json
        assert 'callback' not in params_xml

    def test__make_request(self):
        # same for h_xml
        response = self.h_json._make_request("http://google.com")
        assert response and response.ok


class TestTranslator(GenericTest):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_TRANSLATE")
        assert self.api_key
        self.t_json = Translator(self.api_key)
        assert self.t_json and self.t_json.ok  # check api key is correct
        self.t_xml = Translator(self.api_key, xml=True)
        assert self.t_xml and self.t_xml.ok

    def test_get_langs_json(self):
        langs = self.t_json.get_langs()
        assert langs and isinstance(langs, dict)
        assert 'dirs' in langs
        assert self.t_json._cache
        self.t_json._cache = None
        langs = self.t_json.get_langs()
        assert langs and self.t_json._cache

    def test_get_langs_xml(self):
        langs = self.t_xml.get_langs()
        assert langs and isinstance(langs, list)
        assert self.t_xml._cache
        self.t_xml._cache = None
        langs = self.t_xml.get_langs()
        assert langs and self.t_xml._cache

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented
        # self.t_json._cache = None
        # response = self.t_json.get_langs(callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert not self.t_json._cache
        # assert self._callback_called
        # self._callback_called = False

    def test_directions(self):
        langs = self.t_json.get_langs()
        directions = self.t_json.directions
        assert directions and isinstance(directions, list)
        assert directions == langs['dirs']
        directions = self.t_xml.directions
        assert directions and isinstance(directions, list)

    def test_languages(self):
        langs = self.t_json.get_langs()
        languages = self.t_json.languages
        assert langs and isinstance(langs, dict)
        if 'langs' not in langs:
            return
        assert languages and isinstance(languages, dict)
        assert languages == langs['langs']
        assert self.t_xml.languages is NotImplemented

    def test_ok(self):
        assert self.t_json.ok
        assert self.t_xml.ok

    def test_detect_json(self):
        assert self.assert_exception_happend(
            self.t_json.detect, ValueError, "hello", hint='en'
        )
        guess_lang = self.t_json.detect("hello")
        assert guess_lang and isinstance(guess_lang, str)
        assert guess_lang == 'en'
        guess_lang = self.t_json.detect("gutten", hint=['de'])
        assert guess_lang and guess_lang == 'de'
        guess_lang = self.t_json.detect("hello", post=True)
        assert guess_lang and guess_lang == 'en'

    def test_detect_xml(self):
        assert self.assert_exception_happend(
            self.t_xml.detect, ValueError, "hello", hint='en'
        )
        guess_lang = self.t_xml.detect("hello")
        assert guess_lang is not None
        assert isinstance(guess_lang, ElementTree.Element)
        assert guess_lang.attrib and 'lang' in guess_lang.attrib
        guess_lang = self.t_xml.detect("hello", post=True)
        assert guess_lang is not None
        assert guess_lang.attrib and 'lang' in guess_lang.attrib

    def test_detect_jsonb(self) -> NotImplemented:
        return NotImplemented
        # response = self.t_json.detect("hello", callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert self._callback_called
        # self._callback_called = False

    def test_translate_json(self):
        translation = self.t_json.translate("hello, world", 'de', options=1)
        assert translation and isinstance(translation, dict)
        assert 'code' not in translation and 'detected' in translation
        translation = self.t_json.translate("hello", 'en-de', options=0)
        assert translation and 'detected' not in translation

    def test_translate_xml(self):
        translation = self.t_xml.translate("hello, world", 'de', options=1)
        assert translation and isinstance(translation, ElementTree.Element)

    def test_translate_jsonb(self) -> NotImplemented:
        return NotImplemented
        # response = self.t_json.translate("hello", 'de',
        #                                  callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert self._callback_called
        # self._callback_called = False


class TestDictionary(GenericTest):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_DICT")
        assert self.api_key
        self.v_json = Dictionary(self.api_key)
        assert self.v_json and self.v_json.ok  # check api key is correct
        self.v_xml = Dictionary(self.api_key, xml=True)
        assert self.v_xml and self.v_xml.ok

    def test_get_langs_json(self):
        langs = self.v_json.get_langs()
        assert langs and isinstance(langs, list)
        assert self.v_json._cache
        self.v_json._cache = None
        langs = self.v_json.get_langs()
        assert langs and self.v_json._cache

    def test_get_langs_xml(self):
        langs = self.v_xml.get_langs()
        assert langs and isinstance(langs, list)
        assert self.v_xml._cache
        self.v_xml._cache = None
        langs = self.v_xml.get_langs()
        assert langs and self.v_xml._cache

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented
        # self.v_json._cache = None
        # response = self.v_json.get_langs(callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert not self.v_json._cache
        # assert self._callback_called
        # self._callback_called = False

    def test_ok(self):
        assert self.v_json.ok
        assert self.v_xml.ok

    def test_lookup_json(self):
        assert self.assert_exception_happend(
            self.v_json.lookup, YaTranslateException, "hello", "cpp"
        )
        definition = self.v_json.lookup("hello", 'en-en')
        assert definition and isinstance(definition, dict)
        assert 'head' not in definition and 'def' in definition

    def test_lookup_xml(self):
        exception_happend = False
        try:
            __ = self.v_xml.lookup("hello", 'cpp')
        except YaTranslateException as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        definition = self.v_xml.lookup("hello", 'en-ru')
        assert definition and isinstance(definition, ElementTree.Element)

    def test_lookup_jsonb(self) -> NotImplemented:
        return NotImplemented
        # assert self.assert_exception_happend(
        #     self.v_json.lookup, YaTranslateException, "hello", 'cpp',
        #     callback=self.generic_callback
        # )
        # response = self.v_json.lookup("hello", 'en-en',
        #                               callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert self._callback_called
        # self._callback_called = False

    def test_definitions(self):
        assert self.assert_exception_happend(
            self.v_json.definitions, YaTranslateException, "hello", "cpp"
        )
        assert self.assert_exception_happend(
            self.v_json.definitions, ValueError, "hello", 'en-en',
            callback=self.generic_callback
        )
        assert not self._callback_called
        self._callback_called = False
        definition = self.v_json.definitions("hello", 'en-en')
        assert definition and isinstance(definition, list)
        definition = self.v_xml.definitions("hello", 'en-en')
        assert definition is NotImplemented


class TestPredictor(GenericTest):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_PREDICTOR")
        assert self.api_key
        self.p_json = Predictor(self.api_key)
        assert self.p_json and self.p_json.ok  # check api key is correct
        self.p_xml = Predictor(self.api_key, xml=True)
        assert self.p_xml and self.p_xml.ok

    def test_get_langs_json(self):
        langs = self.p_json.get_langs()
        assert langs and isinstance(langs, list)
        assert self.p_json._cache
        self.p_json._cache = None
        langs = self.p_json.get_langs()
        assert langs and self.p_json._cache

    def test_get_langs_xml(self):
        langs = self.p_xml.get_langs()
        assert langs and isinstance(langs, list)
        assert self.p_xml._cache
        self.p_xml._cache = None
        langs = self.p_xml.get_langs()
        assert langs and self.p_xml._cache

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented
        # self.p_json._cache = None
        # response = self.p_json.get_langs(callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert not self.p_json._cache
        # assert self._callback_called
        # self._callback_called = False

    def test_ok(self):
        assert self.p_json.ok
        assert self.p_xml.ok

    def test_complete_json(self):
        assert self.assert_exception_happend(
            self.p_json.complete, YaTranslateException, "cpp", "#include"
        )
        prediction = self.p_json.complete('en', "hello", limit=1)
        assert prediction and isinstance(prediction, dict)
        assert 'endOfWord' in prediction and prediction['endOfWord']
        assert 'text' in prediction and len(prediction['text']) == 1
        prediction = self.p_json.complete('en', "hel", limit=5)
        assert prediction
        assert 'endOfWord' in prediction and not prediction['endOfWord']
        assert 'text' in prediction and len(prediction['text']) == 5

    def test_complete_xml(self):
        exception_happend = False
        try:
            __ = self.p_xml.complete('cpp', "#includ")
        except YaTranslateException as err:
            logger.debug(err)
            exception_happend = True
        assert exception_happend
        prediction = self.p_xml.complete('en', "hello")
        assert prediction
        assert isinstance(prediction, ElementTree.Element)

    def test_complete_jsonb(self) -> NotImplemented:
        return NotImplemented
        # assert self.assert_exception_happend(
        #     self.p_json.complete, YaTranslateException, "cpp", "#include",
        #     callback=self.generic_callback
        # )
        # response = self.p_json.complete("hello", 'en-en',
        #                                 callback=self.generic_callback)
        # assert response and isinstance(response, requests.Response)
        # assert self._callback_called
        # self._callback_called = False


class TestSpeller(GenericTest):
    def setUp(self):
        self.s_json = Speller()
        assert self.s_json and self.s_json.ok
        self.s_xml = Speller(xml=True)
        assert self.s_xml and self.s_xml.ok

    def test_ok(self):
        assert self.s_json.ok
        assert self.s_xml.ok

    def test__check_json(self):
        assert self.assert_exception_happend(
            self.s_json._check, ValueError, '', ''
        )
        assert self.s_json._check("text", '', post=True) is NotImplemented
        assert self.assert_exception_happend(
            self.s_json._check, YaTranslateException, "text", '', lang=["cpp"]
        )
        suggestion = self.s_json._check("text", "hella")
        assert suggestion and isinstance(suggestion, list)

    def test__check_xml(self):
        assert self.assert_exception_happend(
            self.s_xml._check, ValueError, '', ''
        )
        assert self.s_xml._check("text", '', post=True) is NotImplemented
        assert self.assert_exception_happend(
            self.s_xml._check, YaTranslateException, "text", '', lang=["cpp"]
        )
        suggestion = self.s_xml._check("text", "hella")
        assert suggestion
        assert isinstance(suggestion, ElementTree.Element)

    def test__check_jsonb(self) -> NotImplemented:
        return NotImplemented


if __name__ == "__main__":
    unittest.main()
