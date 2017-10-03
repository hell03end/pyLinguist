from xml.etree import ElementTree

import pytest

from . import Speller, YaTranslateException


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
