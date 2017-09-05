import http
import json
from collections import Callable
from urllib import parse, request
from xml.etree import ElementTree

from .config import logger


class YaTranslateException(Exception):
    """
        Class for possible exceptions during Yandex API usage
    """
    error_codes = {
        400: "Wrong parameter was specified",
        401: "Invalid API key",
        402: "Blocked API key",
        403: "Exceeded the daily limit on the amount of requests",
        404: "Exceeded the daily limit on the amount of translated text",
        413: "Exceeded the maximum text size",
        422: "The text cannot be translated",
        501: "The specified translation direction is not supported",
        503: "Server not available",
    }

    def __init__(self, status_code: int, *args, **kwargs):
        """
        :param status_code: :type int, code, returned from request to API

        >>> YaTranslateException()
        Traceback (most recent call last):
            ...
        TypeError: __init__() missing 1 required positional argument: 'status_code'
        >>> YaTranslateException(400)
        YaTranslateException('Wrong parameter was specified', 400)
        >>> YaTranslateException(300)
        YaTranslateException('Unknown code', 300)
        >>> isinstance(YaTranslateException(400).error_codes, dict)
        True
        """
        message = self.error_codes.get(status_code, "Unknown code")
        super(YaTranslateException, self).__init__(message, status_code,
                                                   *args, **kwargs)


class _YaBaseAPIHandler:
    """
        Generic class for Yandex APIs
    """
    _base_url = r""  # base api url for all requests
    _endpoints = {
        'langs': "getLangs"
    }

    def __init__(self, api_key: str, xml: bool=False, version: str=None):
        """
        :param api_key: :type str, personal API access key, given by Yandex
        :param xml: :type bool, specify returned data format

        >>> _YaBaseAPIHandler()
        Traceback (most recent call last):
            ...
        TypeError: __init__() missing 1 required positional argument: 'api_key'
        >>> _YaBaseAPIHandler('')
        Traceback (most recent call last):
            ...
        YaTranslateException: ('Invalid API key', 401)
        >>> _YaBaseAPIHandler("123")._api_key == "123"
        True
        >>> _YaBaseAPIHandler("123")._json == ".json"
        True
        >>> not _YaBaseAPIHandler("123")._url
        True
        """
        if not api_key:
            raise YaTranslateException(401)
        self._api_key = api_key
        self._json = ".json" if not xml else ""
        self._cache_langs = None
        self._v = version
        self._url = self._base_url

    @property
    def v(self) -> str or NotImplemented:
        if self._v:
            return self._v
        return NotImplemented

    def _make_url(self, endpoint: str, url: str=None) -> str:
        """
        Creates full (base url + endpoint) url for API requests.

        :param endpoint: :type str, one of the keys from self._endpoints dict
        :param url: :type str=None, base url, if not self._url should be used
        :return: :type str, created url for requests

        >>> _YaBaseAPIHandler("123")._make_url('')
        Traceback (most recent call last):
            ...
        KeyError: ''
        >>> _YaBaseAPIHandler("123")._make_url('', "http://url.../") == "http://url.../"
        True
        """
        # not format string for Python less then 3.6 compatibility
        if url:
            return "{}{}".format(url, self._endpoints[endpoint])
        return "{}{}".format(self._url, self._endpoints[endpoint])

    def _form_params(self, **params) -> dict:
        """
        Returns dict of params for request, including API key and etc.

        :param params: :type dict, dict of named params
        :return: :type dict, formed params

        >>> _YaBaseAPIHandler("123")._form_params()
        {'key': '123'}
        >>> 'ui' in _YaBaseAPIHandler("123")._form_params(ui='en')
        True
        >>> 'callback' in _YaBaseAPIHandler("123")._form_params(abs)
        True
        >>> 'callback' not in _YaBaseAPIHandler("123", xml=True)._form_params(abs)
        True
        """
        for key in params:
            if isinstance(params[key], list):
                params[key] = ",".join(params[key])
        parameters = {key: params[key] for key in params
                      if params[key] is not None}
        parameters['key'] = self._api_key
        # for JSONB response
        if 'callback' in parameters and not self._json:
            del parameters['callback']
        return parameters

    def _get_langs(self, base_url: str, update: bool=False, **params) -> ...:
        """
        Wrapper for getLangs API methods.
        Use caching to store received info.

        :param base_url: :type str, base url for requests
        :param update: :type bool=False, update caching values
        :param params: supported additional params: callback, proxies
        :return: :type dict or list or xml.etree.ElementTree.ElementTree or requests.Response
        """
        parameters = {'post': False}
        parameters.update(**self._form_params(**params))
        if "callback" in params:
            return self._make_request(url=self._make_url("langs", base_url),
                                      **parameters)
        if update or not self._cache_langs:
            response = self.make_combined_request(endpoint="langs",
                                                  **parameters)
            if self._json:
                self._cache_langs = response
            elif response.find('dirs'):
                self._cache_langs = [direction.text for direction
                                     in response.find('dirs')]
            else:
                self._cache_langs = [lang.text for lang in response]
        return self._cache_langs

    @staticmethod
    def _make_request_xml(url: str, post: bool=False,
                          **params) -> ElementTree.ElementTree:
        """
        Implements request to API with given params and return content in XML.

        :param url: :type str, prepared url for request to API
        :param post: :type bool, key for making POST request instead GET
        :param params: additional params for request, transmitted throw 'params'
        :return: :type xml.etree.ElementTree.ElementTree, response XML content
        :exception YaTranslateException, requests.exceptions.ConnectionError
        """
        response = _YaBaseAPIHandler._make_request(url, post, **params)
        return ElementTree.fromstring(response.read().decode('utf-8'))

    @staticmethod
    def _make_request_json(url: str, post: bool=False,
                           **params) -> dict or list:
        """
        Implements request to API with given params and return content in JSON.

        :param url: :type str, prepared url for request to API
        :param post: :type bool, key for making POST request instead GET
        :param params: additional params for request, transmitted throw 'params'
        :return: :type dict or list, response content in JSON (response.json())
        :exception YaTranslateException, requests.exceptions.ConnectionError
        """
        response = _YaBaseAPIHandler._make_request(url, post, **params)
        return json.loads(response.read().decode('utf-8'))

    @staticmethod
    def _make_request(url: str, post: bool=False,
                      **params) -> http.client.HTTPResponse:
        """
        Implements request to API with given params.

        :param url: :type str, prepared url for request to API
        :param post: :type bool, key for making POST request instead GET
        :param params: additional params for request, transmitted throw 'params'
        :return: :type request.Response
        :exception YaTranslateException, requests.exceptions.ConnectionError
        """
        url_params = parse.urlencode(params)
        if not post:
            full_url = "{}?{}".format(url, url_params)
            response = request.urlopen(full_url)
        else:
            response = request.urlopen(url, data=url_params.encode('utf-8'))
        if response.code != 200:
            raise YaTranslateException(response.code)
        return response

    def make_combined_request(self, endpoint: str, post: bool=False,
                              **params) -> ...:
        """
        Handle JSON, JSONB and XML requests to API with given params.

        :param endpoint: :type str, one of the keys from self._endpoints dict
        :param post: :type bool, key for making POST request instead GET
        :param params: additional params for request, transmitted throw 'params'
        :return: :type dict or list or request.Response or ElementTree
        :exception YaTranslateException, requests.exceptions.ConnectionError
        """
        parameters = {
            'url': self._make_url(endpoint),
            'post': post
        }
        parameters.update(params)
        if "callback" in params:
            return self._make_request(**parameters)
        elif not self._json:
            return self._make_request_xml(**parameters)
        return self._make_request_json(**parameters)

    def _ok(self, url: str=None, func: Callable=None, *args, **params) -> bool:
        """
        To check that the API key is correct.

        :param url: :type str=None, base url for self._get_langs call
        :param func: :type Callable=None, function to call to test api key
        :param args: :type list, params to pass in called functions
        :param params: :type dict, params to pass in called functions
        :return: :type bool
        """
        try:
            if func:
                __ = func(*args, **params)
            else:
                __ = self._get_langs(url, update=True, *args, **params)
        except http.client.HTTPException as err:
            logger.warning(err)
            return False
        except YaTranslateException as err:
            logger.warning(err)
            return False
        return True


__all__ = ["YaTranslateException"]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
