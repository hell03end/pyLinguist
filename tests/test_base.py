import pytest

from pyLinguist import YaBaseAPIHandler, YaTranslateException


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
