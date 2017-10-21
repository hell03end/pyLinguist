import os
from xml.etree import ElementTree

import pytest

from pyLinguist import Predictor, YaTranslateException


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
