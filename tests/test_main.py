import os
import unittest
import requests
from xml.etree import ElementTree

from pyLinguist import (
    Translator, Dictionary, Predictor, Speller, YaTranslateException,
    _YaBaseAPIHandler, logger
)
from .commons import GenericTest


class TestBaseTypes(GenericTest):
    def setUp(self):
        with self.assertRaises(YaTranslateException):
            __ = _YaBaseAPIHandler(None)
        self.api_key = "123"
        self.h_json = _YaBaseAPIHandler(self.api_key)
        self.assertTrue(self.h_json)
        self.h_xml = _YaBaseAPIHandler(self.api_key, xml=True)
        self.assertTrue(self.h_xml)

    def test_attrib_json(self):
        self.assertTrue(self.h_json._api_key)
        self.assertTrue(self.h_json._json)
        self.assertFalse(self.h_json._cache_langs)
        self.assertFalse(self.h_json._url)
        self.assertFalse(self.h_json._v)
        self.assertIs(self.h_json.v, NotImplemented)
        self.h_json._v = '1'
        self.assertEqual(self.h_json.v, '1')

    def test_attrib_xml(self):
        self.assertTrue(self.h_xml._api_key)
        self.assertFalse(self.h_xml._json)
        self.assertFalse(self.h_xml._cache_langs)
        self.assertFalse(self.h_xml._url)
        self.assertFalse(self.h_xml._v)
        self.assertIs(self.h_xml.v, NotImplemented)
        self.h_xml._v = '1'
        self.assertEqual(self.h_xml.v, '1')

    def test__make_url(self):
        # same for h_xml
        base_url = "http://google.com/"
        url = self.h_json._make_url("langs")
        self.assertTrue(url)
        self.assertEqual(url, self.h_json._url +
                         self.h_json._endpoints['langs'])
        with self.assertRaises(KeyError):
            __ = self.h_json._make_url('')
        url = self.h_json._make_url('langs', base_url)
        self.assertTrue(url)
        self.assertEqual(url, base_url + self.h_json._endpoints['langs'])

    def test__form_params(self):
        params = {
            'a': 1,
            'b': 2
        }
        params_json = self.h_json._form_params(**params)
        self.assertTrue(params_json)
        self.assertIsInstance(params_json, dict)
        self.assertIn('key', params_json)
        self.assertIn('a', params_json)
        self.assertIn('b', params_json)
        self.assertEqual(params['a'], params_json['a'])
        self.assertEqual(params['b'], params_json['b'])
        params_xml = self.h_xml._form_params(**params)
        self.assertTrue(params_xml)
        self.assertIsInstance(params_xml, dict)
        self.assertIn('key', params_xml)
        self.assertIn('a', params_xml)
        self.assertIn('b', params_xml)
        self.assertEqual(params['a'], params_xml['a'])
        self.assertEqual(params['b'], params_xml['b'])
        params.update({'callback': self.generic_callback})
        params_json = self.h_json._form_params(**params)
        params_xml = self.h_xml._form_params(**params)
        self.assertIn('callback', params_json)
        self.assertNotIn('callback', params_xml)

    def test__make_request(self):
        # same for h_xml
        response = self.h_json._make_request("http://google.com")
        self.assertTrue(response)
        self.assertEqual(response.code, 200)


class TestTranslator(GenericTest):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_TRANSLATE")
        self.assertTrue(self.api_key)
        self.t_json = Translator(self.api_key)
        self.assertTrue(self.t_json)
        self.assertTrue(self.t_json.ok)  # check api key is correct
        self.t_xml = Translator(self.api_key, xml=True)
        self.assertTrue(self.t_xml)
        self.assertTrue(self.t_xml.ok)

    def test_get_langs_json(self):
        langs = self.t_json.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, dict)
        self.assertIn('dirs', langs)
        self.assertTrue(self.t_json._cache_langs)
        self.t_json._cache_langs = None
        langs = self.t_json.get_langs()
        self.assertTrue(langs)
        self.assertTrue(self.t_json._cache_langs)

    def test_get_langs_xml(self):
        langs = self.t_xml.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, list)
        self.assertTrue(self.t_xml._cache_langs)
        self.t_xml._cache_langs = None
        langs = self.t_xml.get_langs()
        self.assertTrue(langs)
        self.assertTrue(self.t_xml._cache_langs)

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_directions(self):
        langs = self.t_json.get_langs()
        directions = self.t_json.directions
        self.assertTrue(directions)
        self.assertIsInstance(directions, list)
        self.assertEqual(directions, langs['dirs'])
        directions = self.t_xml.directions
        self.assertTrue(directions)
        self.assertIsInstance(directions, list)

    def test_languages(self):
        langs = self.t_json.get_langs()
        languages = self.t_json.languages
        self.assertTrue(langs)
        self.assertIsInstance(langs, dict)
        if 'langs' not in langs:
            return
        self.assertTrue(languages)
        self.assertIsInstance(languages, dict)
        self.assertEqual(languages, langs['langs'])
        self.assertIs(self.t_xml.languages, NotImplemented)

    def test_ok(self):
        self.assertTrue(self.t_json.ok)
        self.assertTrue(self.t_xml.ok)

    def test_detect_json(self):
        with self.assertRaises(ValueError):
            __ = self.t_json.detect("hello", hint='en')
        guess_lang = self.t_json.detect("hello")
        self.assertTrue(guess_lang)
        self.assertIsInstance(guess_lang, str)
        self.assertEqual(guess_lang, 'en')
        guess_lang = self.t_json.detect("gutten", hint=['de'])
        self.assertTrue(guess_lang)
        self.assertEqual(guess_lang, 'de')
        guess_lang = self.t_json.detect("hello", post=True)
        self.assertTrue(guess_lang)
        self.assertEqual(guess_lang, 'en')

    def test_detect_xml(self):
        with self.assertRaises(ValueError):
            __ = self.t_xml.detect("hello", hint='en')
        guess_lang = self.t_xml.detect("hello")
        self.assertIsNotNone(guess_lang)
        self.assertIsInstance(guess_lang, ElementTree.Element)
        self.assertTrue(guess_lang.attrib)
        self.assertIn('lang', guess_lang.attrib)
        guess_lang = self.t_xml.detect("hello", post=True)
        self.assertIsNotNone(guess_lang)
        self.assertTrue(guess_lang.attrib)
        self.assertIn('lang', guess_lang.attrib)

    def test_detect_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_translate_json(self):
        translation = self.t_json.translate("hello, world", 'de', options=1)
        self.assertTrue(translation)
        self.assertIsInstance(translation, dict)
        self.assertNotIn('code', translation)
        self.assertIn('detected', translation)
        translation = self.t_json.translate("hello", 'en-de', options=0)
        self.assertTrue(translation)
        self.assertNotIn('detected', translation)
        translation = self.t_json.translate(["hello", "world", "cat"], 'de')
        self.assertTrue(translation)
        self.assertIn('text', translation)
        self.assertIsInstance(translation['text'], list)
        self.assertTrue(len(translation['text']) == 3)
        translation = self.t_json.translate(['hello, "abs"', 'cat'], 'de')
        self.assertTrue(translation)
        self.assertIn('text', translation)
        self.assertIsInstance(translation['text'], list)
        self.assertTrue(len(translation['text']) == 2)

    def test_translate_xml(self):
        translation = self.t_xml.translate("hello, world", 'de', options=1)
        self.assertTrue(translation)
        self.assertIsInstance(translation, ElementTree.Element)

    def test_translate_jsonb(self) -> NotImplemented:
        return NotImplemented


class TestDictionary(GenericTest):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_DICT")
        self.assertTrue(self.api_key)
        self.v_json = Dictionary(self.api_key)
        self.assertTrue(self.v_json)
        self.assertTrue(self.v_json.ok)  # check api key is correct
        self.v_xml = Dictionary(self.api_key, xml=True)
        self.assertTrue(self.v_xml)
        self.assertTrue(self.v_xml.ok)

    def test_get_langs_json(self):
        langs = self.v_json.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, list)
        self.assertTrue(self.v_json._cache_langs)
        self.v_json._cache_langs = None
        langs = self.v_json.get_langs()
        self.assertTrue(langs)
        self.assertTrue(self.v_json._cache_langs)

    def test_get_langs_xml(self):
        langs = self.v_xml.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, list)
        self.assertTrue(self.v_xml._cache_langs)
        self.v_xml._cache_langs = None
        langs = self.v_xml.get_langs()
        self.assertTrue(langs)
        self.assertTrue(self.v_xml._cache_langs)

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_ok(self):
        self.assertTrue(self.v_json.ok)
        self.assertTrue(self.v_xml.ok)

    def test_lookup_json(self):
        with self.assertRaises(YaTranslateException):
            __ = self.v_json.lookup("hello", "cpp")
        definition = self.v_json.lookup("hello", 'en-en')
        self.assertTrue(definition)
        self.assertIsInstance(definition, dict)
        self.assertNotIn('head', definition)
        self.assertIn('def', definition)

    def test_lookup_xml(self):
        with self.assertRaises(YaTranslateException):
            __ = self.v_xml.lookup("hello", 'cpp')
        definition = self.v_xml.lookup("hello", 'en-ru')
        self.assertTrue(definition)
        self.assertIsInstance(definition, ElementTree.Element)

    def test_lookup_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_definitions(self):
        with self.assertRaises(YaTranslateException):
            __ = self.v_json.definitions("hello", "cpp")
        with self.assertRaises(ValueError):
            __ = self.v_json.definitions("hello", 'en-en',
                                         callback=self.generic_callback)
        self.assertFalse(self._callback_called)
        self._callback_called = False
        definition = self.v_json.definitions("hello", 'en-en')
        self.assertTrue(definition)
        self.assertIsInstance(definition, list)
        definition = self.v_xml.definitions("hello", 'en-en')
        self.assertIs(definition, NotImplemented)


class TestPredictor(GenericTest):
    def setUp(self):
        self.api_key = os.environ.get("API_KEY_YA_PREDICTOR")
        self.assertTrue(self.api_key)
        self.p_json = Predictor(self.api_key)
        self.assertTrue(self.p_json)
        self.assertTrue(self.p_json.ok)  # check api key is correct
        self.p_xml = Predictor(self.api_key, xml=True)
        self.assertTrue(self.p_xml)
        self.assertTrue(self.p_xml.ok)

    def test_get_langs_json(self):
        langs = self.p_json.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, list)
        self.assertTrue(self.p_json._cache_langs)
        self.p_json._cache_langs = None
        langs = self.p_json.get_langs()
        self.assertTrue(langs)
        self.assertTrue(self.p_json._cache_langs)

    def test_get_langs_xml(self):
        langs = self.p_xml.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, list)
        self.assertTrue(self.p_xml._cache_langs)
        self.p_xml._cache_langs = None
        langs = self.p_xml.get_langs()
        self.assertTrue(langs)
        self.assertTrue(self.p_xml._cache_langs)

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_ok(self):
        self.assertTrue(self.p_json.ok)
        self.assertTrue(self.p_xml.ok)

    def test_complete_json(self):
        with self.assertRaises(YaTranslateException):
            __ = self.p_json.complete("cpp", "#include")
        prediction = self.p_json.complete('en', "hello", limit=1)
        self.assertTrue(prediction)
        self.assertIsInstance(prediction, dict)
        self.assertIn('endOfWord', prediction)
        self.assertTrue(prediction['endOfWord'])
        self.assertIn('text', prediction)
        self.assertEqual(len(prediction['text']), 1)
        prediction = self.p_json.complete('en', "hel", limit=5)
        self.assertTrue(prediction)
        self.assertIn('endOfWord', prediction)
        self.assertFalse(prediction['endOfWord'])
        self.assertIn('text', prediction)
        self.assertEqual(len(prediction['text']), 5)

    def test_complete_xml(self):
        with self.assertRaises(YaTranslateException):
            __ = self.p_xml.complete('cpp', "#include")
        prediction = self.p_xml.complete('en', "hello")
        self.assertTrue(prediction)
        self.assertIsInstance(prediction, ElementTree.Element)

    def test_complete_jsonb(self) -> NotImplemented:
        return NotImplemented


class TestSpeller(GenericTest):
    def setUp(self):
        self.s_json = Speller()
        self.assertTrue(self.s_json)
        self.assertTrue(self.s_json.ok)
        self.s_xml = Speller(xml=True)
        self.assertTrue(self.s_xml)
        self.assertTrue(self.s_xml.ok)

    def test_get_langs(self):
        langs = self.s_json.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, set)
        langs = self.s_xml.get_langs()
        self.assertTrue(langs)
        self.assertIsInstance(langs, set)

    def test_ok(self):
        self.assertTrue(self.s_json.ok)
        self.assertTrue(self.s_xml.ok)

    def test__check_json(self):
        with self.assertRaises(ValueError):
            __ = self.s_json._check('', '')
        self.assertIs(self.s_json._check("text", '', post=True),
                      NotImplemented)
        with self.assertRaises(YaTranslateException):
            __ = self.s_json._check("text", '', lang=["cpp"])
        suggestion = self.s_json._check("text", "hella")
        self.assertTrue(suggestion)
        self.assertIsInstance(suggestion, list)

    def test__check_xml(self):
        with self.assertRaises(ValueError):
            __ = self.s_xml._check('', '')
        self.assertIs(self.s_xml._check("text", '', post=True), NotImplemented)
        with self.assertRaises(YaTranslateException):
            __ = self.s_xml._check("text", '', lang=["cpp"])
        suggestion = self.s_xml._check("text", "hella")
        self.assertTrue(suggestion)
        self.assertIsInstance(suggestion, ElementTree.Element)

    def test__check_jsonb(self) -> NotImplemented:
        return NotImplemented


if __name__ == "__main__":
    unittest.main()
