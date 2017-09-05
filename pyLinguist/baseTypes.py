import http
import json
from collections import Callable, Collection
from urllib import parse, request
from xml.etree import ElementTree

from .config import logger


class YaTranslateException(Exception):
    """Class for possible exceptions during Yandex API usage"""
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
        message = self.error_codes.get(status_code, "Unknown code")
        super(YaTranslateException, self).__init__(message, status_code,
                                                   *args, **kwargs)


class _YaBaseAPIHandler:
    """Generic class for Yandex APIs"""
    _base_url = r""  # base api url for all requests
    _endpoints = {
        'langs': "getLangs"
    }

    def __init__(self, api_key: str, xml: bool=False, version: str=None):
        if not api_key:
            raise YaTranslateException(401)
        self._api_key = api_key
        self._json = ".json" if not xml else ""
        self._cache_langs = None
        self._v = version
        self._url = self._base_url

    @property
    def v(self) -> str or NotImplemented:
        """API version"""
        if self._v:
            return self._v
        return NotImplemented

    def _make_url(self, endpoint: str, url: str=None) -> str:
        """Creates full (base url + endpoint) url for API requests."""
        # not format string for Python less then 3.6 compatibility
        if url:
            return "{}{}".format(url, self._endpoints[endpoint])
        return "{}{}".format(self._url, self._endpoints[endpoint])

    def _form_params(self, list_exceptions: Collection={}, **params) -> dict:
        """Returns dict of params for request, including API key and etc."""
        for key in params:
            if isinstance(params[key], list) and key not in list_exceptions:
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
        """
        response = _YaBaseAPIHandler._make_request(url, post, **params)
        return ElementTree.fromstring(response.read().decode('utf-8'))

    @staticmethod
    def _make_request_json(url: str, post: bool=False,
                           **params) -> Collection:
        """
        Implements request to API with given params and return content in JSON.
        """
        response = _YaBaseAPIHandler._make_request(url, post, **params)
        return json.loads(response.read().decode('utf-8'))

    @staticmethod
    def _make_request(url: str, post: bool=False,
                      **params) -> http.client.HTTPResponse:
        """Implements request to API with given params."""
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
        """Handle JSON, JSONB and XML requests to API with given params."""
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
        """To check that the API key is correct."""
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
