import os
import pytest
import requests
from xml.etree import ElementTree

from pyLinguist import (
    Translator, Dictionary, Predictor, Speller, YaTranslateException,
    YaBaseAPIHandler
)


class TestBaseTypes:
    def setup_class(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = YaBaseAPIHandler(None)
        self.api_key = "123"
        self.h_json = YaBaseAPIHandler(self.api_key)
        assert self.h_json
        self.h_xml = YaBaseAPIHandler(self.api_key, xml=True)
        assert self.h_xml

    def test_attrib_json(self):
        assert self.h_json._api_key
        assert self.h_json._json
        assert not self.h_json._cache_langs
        assert not self.h_json._url
        assert not self.h_json._v
        assert self.h_json.v is NotImplemented
        self.h_json._v = '1'
        assert self.h_json.v == '1'

    def test_attrib_xml(self):
        assert self.h_xml._api_key
        assert not self.h_xml._json
        assert not self.h_xml._cache_langs
        assert not self.h_xml._url
        assert not self.h_xml._v
        self.h_xml.v is NotImplemented
        self.h_xml._v = '1'
        assert self.h_xml.v == '1'

    def test__make_url(self):
        # same for h_xml
        base_url = "http://google.com/"
        url = self.h_json._make_url("langs")
        assert url
        assert url == self.h_json._url + self.h_json._endpoints['langs']
        with pytest.raises(KeyError) as excinfo:
            assert excinfo
            __ = self.h_json._make_url('')
        url = self.h_json._make_url('langs', base_url)
        assert url
        assert url == base_url + self.h_json._endpoints['langs']

    def test__form_params(self):
        params = {
            'a': 1,
            'b': 2
        }
        params_json = self.h_json._form_params(**params)
        assert params_json
        assert isinstance(params_json, dict)
        assert 'key' in params_json
        assert 'a' in params_json
        assert 'b' in params_json
        assert params['a'] == params_json['a']
        assert params['b'] == params_json['b']
        params_xml = self.h_xml._form_params(**params)
        assert params_xml
        assert isinstance(params_xml, dict)
        assert 'key' in params_xml
        assert 'a' in params_xml
        assert 'b' in params_xml
        assert params['a'] == params_xml['a']
        assert params['b'] == params_xml['b']
        params.update({'callback': lambda: None})
        params_json = self.h_json._form_params(**params)
        params_xml = self.h_xml._form_params(**params)
        assert 'callback' in params_json
        assert 'callback' not in params_xml

    def test__make_request(self):
        # same for h_xml
        response = self.h_json._make_request("http://google.com")
        assert response
        assert response.code == 200


class TestTranslator:
    def setup_class(self):
        self.api_key = os.environ.get("API_KEY_YA_TRANSLATE")
        assert self.api_key
        self.t_json = Translator(self.api_key)
        assert self.t_json
        assert self.t_json.ok
        self.t_xml = Translator(self.api_key, xml=True)
        assert self.t_xml
        assert self.t_xml.ok

    def test_get_langs_json(self):
        langs = self.t_json.get_langs()
        assert langs
        assert isinstance(langs, dict)
        assert 'dirs' in langs
        assert self.t_json._cache_langs
        self.t_json._cache_langs = None
        langs = self.t_json.get_langs()
        assert langs
        assert self.t_json._cache_langs

    def test_get_langs_xml(self):
        langs = self.t_xml.get_langs()
        assert langs
        assert isinstance(langs, list)
        assert self.t_xml._cache_langs
        self.t_xml._cache_langs = None
        langs = self.t_xml.get_langs()
        assert langs
        assert self.t_xml._cache_langs

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_directions(self):
        langs = self.t_json.get_langs()
        directions = self.t_json.directions
        assert directions
        assert isinstance(directions, list)
        assert directions == langs['dirs']
        directions = self.t_xml.directions
        assert directions
        assert isinstance(directions, list)

    def test_languages(self):
        langs = self.t_json.get_langs()
        languages = self.t_json.languages
        assert langs
        assert isinstance(langs, dict)
        if 'langs' not in langs:
            return
        assert languages
        assert isinstance(languages, dict)
        assert languages == langs['langs']
        assert self.t_xml.languages is NotImplemented

    def test_ok(self):
        assert self.t_json.ok
        assert self.t_xml.ok

    def test_detect_json(self):
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.t_json.detect("hello", hint='en')
        guess_lang = self.t_json.detect("hello")
        assert guess_lang
        assert isinstance(guess_lang, str)
        assert guess_lang == 'en'
        guess_lang = self.t_json.detect("gutten", hint=['de'])
        assert guess_lang
        assert guess_lang == 'de'
        guess_lang = self.t_json.detect("hello", post=True)
        assert guess_lang
        assert guess_lang == 'en'

    def test_detect_xml(self):
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.t_xml.detect("hello", hint='en')
        guess_lang = self.t_xml.detect("hello")
        assert guess_lang is not None
        assert isinstance(guess_lang, ElementTree.Element)
        assert guess_lang.attrib
        assert 'lang' in guess_lang.attrib
        guess_lang = self.t_xml.detect("hello", post=True)
        assert guess_lang is not None
        assert guess_lang.attrib
        assert 'lang' in guess_lang.attrib

    def test_detect_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_translate_json(self):
        translation = self.t_json.translate("hello, world", 'de', options=1)
        assert translation
        assert isinstance(translation, dict)
        assert 'code' not in translation
        assert 'detected' in translation
        translation = self.t_json.translate("hello", 'en-de', options=0)
        assert translation
        assert 'detected' not in translation
        translation = self.t_json.translate(["hello", "world", "cat"], 'de')
        assert translation
        assert 'text' in translation
        assert isinstance(translation['text'], list)
        # assert len(translation['text']) == 3  # until not realized
        translation = self.t_json.translate(['hello, "abs"', 'cat'], 'de')
        assert translation
        assert 'text' in translation
        assert isinstance(translation['text'], list)
        # assert len(translation['text']) == 2)

    def test_translate_xml(self):
        translation = self.t_xml.translate("hello, world", 'de', options=1)
        assert translation
        assert isinstance(translation, ElementTree.Element)

    def test_translate_jsonb(self) -> NotImplemented:
        return NotImplemented


class TestDictionary:
    def setup_class(self):
        self.api_key = os.environ.get("API_KEY_YA_DICT")
        assert self.api_key
        self.v_json = Dictionary(self.api_key)
        assert self.v_json
        assert self.v_json.ok
        self.v_xml = Dictionary(self.api_key, xml=True)
        assert self.v_xml
        assert self.v_xml.ok

    def test_get_langs_json(self):
        langs = self.v_json.get_langs()
        assert langs
        assert isinstance(langs, list)
        assert self.v_json._cache_langs
        self.v_json._cache_langs = None
        langs = self.v_json.get_langs()
        assert langs
        assert self.v_json._cache_langs

    def test_get_langs_xml(self):
        langs = self.v_xml.get_langs()
        assert langs
        assert isinstance(langs, list)
        assert self.v_xml._cache_langs
        self.v_xml._cache_langs = None
        langs = self.v_xml.get_langs()
        assert langs
        assert self.v_xml._cache_langs

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_ok(self):
        assert self.v_json.ok
        assert self.v_xml.ok

    def test_lookup_json(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.v_json.lookup("hello", "cpp")
        definition = self.v_json.lookup("hello", 'en-en')
        assert definition
        assert isinstance(definition, dict)
        assert 'head' not in definition
        assert 'def' in definition

    def test_lookup_xml(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.v_xml.lookup("hello", 'cpp')
        definition = self.v_xml.lookup("hello", 'en-ru')
        assert definition
        assert isinstance(definition, ElementTree.Element)

    def test_lookup_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_definitions(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.v_json.definitions("hello", "cpp")
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.v_json.definitions("hello", 'en-en',
                                         callback=lambda: None)
        definition = self.v_json.definitions("hello", 'en-en')
        assert definition
        assert isinstance(definition, list)
        definition = self.v_xml.definitions("hello", 'en-en')
        assert definition is NotImplemented


class TestPredictor:
    def setup_class(self):
        self.api_key = os.environ.get("API_KEY_YA_PREDICTOR")
        assert self.api_key
        self.p_json = Predictor(self.api_key)
        assert self.p_json
        assert self.p_json.ok
        self.p_xml = Predictor(self.api_key, xml=True)
        assert self.p_xml
        assert self.p_xml.ok

    def test_get_langs_json(self):
        langs = self.p_json.get_langs()
        assert langs
        assert isinstance(langs, list)
        assert self.p_json._cache_langs
        self.p_json._cache_langs = None
        langs = self.p_json.get_langs()
        assert langs
        assert self.p_json._cache_langs

    def test_get_langs_xml(self):
        langs = self.p_xml.get_langs()
        assert langs
        assert isinstance(langs, list)
        assert self.p_xml._cache_langs
        self.p_xml._cache_langs = None
        langs = self.p_xml.get_langs()
        assert langs
        assert self.p_xml._cache_langs

    def test_get_langs_jsonb(self) -> NotImplemented:
        return NotImplemented

    def test_ok(self):
        assert self.p_json.ok
        assert self.p_xml.ok

    def test_complete_json(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.p_json.complete("cpp", "#include")
        prediction = self.p_json.complete('en', "hello", limit=1)
        assert prediction
        assert isinstance(prediction, dict)
        assert 'endOfWord' in prediction
        assert prediction['endOfWord']
        assert 'text' in prediction
        assert len(prediction['text']) == 1
        prediction = self.p_json.complete('en', "hel", limit=5)
        assert prediction
        assert 'endOfWord' in prediction
        assert not prediction['endOfWord']
        assert 'text' in prediction
        assert len(prediction['text']) == 5

    def test_complete_xml(self):
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.p_xml.complete('cpp', "#include")
        prediction = self.p_xml.complete('en', "hello")
        assert prediction
        assert isinstance(prediction, ElementTree.Element)

    def test_complete_jsonb(self) -> NotImplemented:
        return NotImplemented


class TestSpeller:
    def setup_class(self):
        self.s_json = Speller()
        assert self.s_json
        assert self.s_json.ok
        self.s_xml = Speller(xml=True)
        assert self.s_xml
        assert self.s_xml.ok

    def test_get_langs(self):
        langs = self.s_json.get_langs()
        assert langs
        assert isinstance(langs, set)
        langs = self.s_xml.get_langs()
        assert langs
        assert isinstance(langs, set)

    def test_ok(self):
        assert self.s_json.ok
        assert self.s_xml.ok

    def test__check_json(self):
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.s_json._check('', '')
        assert self.s_json._check("text", '', post=True) is NotImplemented
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.s_json._check("text", '', lang=["cpp"])
        suggestion = self.s_json._check("text", "hella")
        assert suggestion
        assert isinstance(suggestion, list)

    def test__check_xml(self):
        with pytest.raises(ValueError) as excinfo:
            assert excinfo
            __ = self.s_xml._check('', '')
        assert self.s_xml._check("text", '', post=True) is NotImplemented
        with pytest.raises(YaTranslateException) as excinfo:
            assert excinfo
            __ = self.s_xml._check("text", '', lang=["cpp"])
        suggestion = self.s_xml._check("text", "hella")
        assert suggestion
        assert isinstance(suggestion, ElementTree.Element)

    def test__check_jsonb(self) -> NotImplemented:
        return NotImplemented
