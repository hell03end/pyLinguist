import os
from xml.etree import ElementTree

import pytest

from pyLinguist import Dictionary, YaTranslateException


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
