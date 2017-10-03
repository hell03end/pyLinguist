import os
from xml.etree import ElementTree

import pytest

from . import Translator, YaTranslateException


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
